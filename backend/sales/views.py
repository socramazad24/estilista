"""
Sales views for estilera project.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Client, Sale, SaleItem, DailyCashRegister
from .serializers import (
    ClientSerializer, ClientListSerializer, SaleSerializer, 
    SaleCreateSerializer, SaleListSerializer, DailyCashRegisterSerializer,
    SalesReportSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClientListSerializer
        return ClientSerializer
    
    @action(detail=False, methods=['get'])
    def frequent(self, request):
        clients = Client.objects.annotate(
            sales_count=Count('sales')
        ).filter(sales_count__gte=3).order_by('-sales_count')[:10]
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['invoice_number', 'client__first_name', 'client__last_name']
    filterset_fields = ['status', 'payment_method', 'stylist']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SaleCreateSerializer
        elif self.action == 'list':
            return SaleListSerializer
        return SaleSerializer
    
    def get_queryset(self):
        return Sale.objects.select_related('client', 'stylist', 'cashier').prefetch_related('items', 'items__service')
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        sales = self.get_queryset().filter(date__date=today, status='completed')
        serializer = SaleListSerializer(sales, many=True)
        
        total = sales.aggregate(total=Sum('total'))['total'] or 0
        count = sales.count()
        
        return Response({
            'sales': serializer.data,
            'total_amount': total,
            'count': count
        })
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        period = request.query_params.get('period', 'month')
        
        now = timezone.now()
        if period == 'day':
            start_date = now.date()
            end_date = start_date + timedelta(days=1)
        elif period == 'week':
            start_date = now.date() - timedelta(days=now.weekday())
            end_date = start_date + timedelta(days=7)
        elif period == 'month':
            start_date = now.replace(day=1).date()
            if now.month == 12:
                end_date = now.replace(year=now.year + 1, month=1, day=1).date()
            else:
                end_date = now.replace(month=now.month + 1, day=1).date()
        else:
            start_date = now.replace(day=1, month=1).date()
            end_date = now.replace(year=now.year + 1, day=1, month=1).date()
        
        sales = Sale.objects.filter(
            date__date__gte=start_date,
            date__date__lt=end_date,
            status='completed'
        )
        
        total_sales = sales.count()
        total_amount = sales.aggregate(total=Sum('total'))['total'] or 0
        average_sale = total_amount / total_sales if total_sales > 0 else 0
        
        # By payment method
        by_payment = sales.values('payment_method').annotate(
            count=Count('id'),
            amount=Sum('total')
        )
        by_payment_dict = {item['payment_method']: {'count': item['count'], 'amount': item['amount']} 
                          for item in by_payment}
        
        # By service
        from services.models import Service
        by_service = Service.objects.filter(
            sale_items__sale__in=sales
        ).annotate(
            count=Count('sale_items'),
            total=Sum('sale_items__total')
        ).order_by('-count')[:10]
        
        by_service_list = [{'name': s.name, 'count': s.count, 'total': s.total} for s in by_service]
        
        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'total_sales': total_sales,
            'total_amount': total_amount,
            'average_sale': average_sale,
            'by_payment_method': by_payment_dict,
            'by_service': by_service_list
        })
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        now = timezone.now()
        
        # Today
        today_sales = Sale.objects.filter(date__date=now.date(), status='completed')
        today_total = today_sales.aggregate(total=Sum('total'))['total'] or 0
        today_count = today_sales.count()
        
        # This week
        week_start = now.date() - timedelta(days=now.weekday())
        week_sales = Sale.objects.filter(date__date__gte=week_start, status='completed')
        week_total = week_sales.aggregate(total=Sum('total'))['total'] or 0
        
        # This month
        month_start = now.replace(day=1).date()
        month_sales = Sale.objects.filter(date__date__gte=month_start, status='completed')
        month_total = month_sales.aggregate(total=Sum('total'))['total'] or 0
        
        # Top services
        from services.models import Service
        top_services = Service.objects.filter(
            sale_items__sale__date__date__gte=month_start,
            sale_items__sale__status='completed'
        ).annotate(
            count=Count('sale_items')
        ).order_by('-count')[:5]
        
        top_services_data = [{'name': s.name, 'count': s.count} for s in top_services]
        
        return Response({
            'today': {'total': today_total, 'count': today_count},
            'week': {'total': week_total},
            'month': {'total': month_total},
            'top_services': top_services_data
        })


class DailyCashRegisterViewSet(viewsets.ModelViewSet):
    queryset = DailyCashRegister.objects.all()
    serializer_class = DailyCashRegisterSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailyCashRegister.objects.select_related('opened_by', 'closed_by')
    
    @action(detail=False, methods=['post'])
    def open(self, request):
        today = timezone.now().date()
        
        if DailyCashRegister.objects.filter(date=today, status='open').exists():
            return Response(
                {'error': 'Ya existe una caja abierta para hoy'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cash_register = DailyCashRegister.objects.create(
            date=today,
            opening_amount=request.data.get('opening_amount', 0),
            opened_by=request.user
        )
        
        serializer = self.get_serializer(cash_register)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        cash_register = self.get_object()
        
        if cash_register.status == 'closed':
            return Response(
                {'error': 'La caja ya está cerrada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate totals from today's sales
        today_sales = Sale.objects.filter(
            date__date=cash_register.date,
            status='completed'
        )
        
        cash_register.total_sales = today_sales.aggregate(total=Sum('total'))['total'] or 0
        cash_register.total_cash = today_sales.filter(payment_method='cash').aggregate(total=Sum('total'))['total'] or 0
        cash_register.total_card = today_sales.filter(payment_method='card').aggregate(total=Sum('total'))['total'] or 0
        cash_register.total_transfer = today_sales.filter(payment_method='transfer').aggregate(total=Sum('total'))['total'] or 0
        cash_register.total_other = today_sales.filter(payment_method__in=['nequi', 'daviplata', 'other']).aggregate(total=Sum('total'))['total'] or 0
        
        cash_register.closing_amount = request.data.get('closing_amount', 0)
        cash_register.closed_by = request.user
        cash_register.status = 'closed'
        cash_register.closed_at = timezone.now()
        cash_register.save()
        
        serializer = self.get_serializer(cash_register)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        today = timezone.now().date()
        try:
            cash_register = DailyCashRegister.objects.get(date=today, status='open')
            serializer = self.get_serializer(cash_register)
            return Response(serializer.data)
        except DailyCashRegister.DoesNotExist:
            return Response({'is_open': False})
