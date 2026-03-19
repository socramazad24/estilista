"""
Employees views for estilera project.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, EmployeeLoan, LoanPayment, EmployeeAttendance, EmployeeCommission
from .serializers import (
    EmployeeSerializer, EmployeeListSerializer, EmployeeLoanSerializer,
    EmployeeLoanCreateSerializer, EmployeeAttendanceSerializer, EmployeeCommissionSerializer
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'document_number', 'email']
    filterset_fields = ['status', 'contract_type']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        employees = Employee.objects.filter(status='active')
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def loans(self, request, pk=None):
        employee = self.get_object()
        loans = employee.loans.all()
        serializer = EmployeeLoanSerializer(loans, many=True)
        return Response(serializer.data)


class EmployeeLoanViewSet(viewsets.ModelViewSet):
    queryset = EmployeeLoan.objects.all()
    serializer_class = EmployeeLoanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['employee__first_name', 'employee__last_name']
    filterset_fields = ['status']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeLoanCreateSerializer
        return EmployeeLoanSerializer
    
    def get_queryset(self):
        return EmployeeLoan.objects.select_related('employee', 'approved_by').prefetch_related('payments')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        loans = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        from django.db.models import Sum
        
        active_loans = EmployeeLoan.objects.filter(status='active')
        total_active = active_loans.count()
        total_amount = active_loans.aggregate(total=Sum('remaining_amount'))['total'] or 0
        
        return Response({
            'total_active_loans': total_active,
            'total_remaining_amount': total_amount
        })
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        loan = self.get_object()
        if loan.status != 'active':
            return Response({'error': 'El préstamo no está activo'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils import timezone
        loan.approval_date = timezone.now().date()
        loan.approved_by = request.user
        loan.save()
        
        serializer = self.get_serializer(loan)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def register_payment(self, request, pk=None):
        loan = self.get_object()
        if loan.status != 'active':
            return Response({'error': 'El préstamo no está activo'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_id = request.data.get('payment_id')
        try:
            payment = LoanPayment.objects.get(id=payment_id, loan=loan)
            if payment.is_paid:
                return Response({'error': 'La cuota ya está pagada'}, status=status.HTTP_400_BAD_REQUEST)
            
            from django.utils import timezone
            payment.is_paid = True
            payment.paid_date = timezone.now().date()
            payment.save()
            
            loan.remaining_amount -= payment.amount
            loan.paid_installments += 1
            
            if loan.remaining_amount <= 0:
                loan.status = 'paid'
            
            loan.save()
            
            serializer = self.get_serializer(loan)
            return Response(serializer.data)
        except LoanPayment.DoesNotExist:
            return Response({'error': 'Cuota no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class EmployeeAttendanceViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAttendance.objects.all()
    serializer_class = EmployeeAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['employee__first_name', 'employee__last_name']
    filterset_fields = ['status', 'employee']
    
    def get_queryset(self):
        return EmployeeAttendance.objects.select_related('employee')
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        attendances = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def check_in(self, request):
        from django.utils import timezone
        
        employee_id = request.data.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
            attendance, created = EmployeeAttendance.objects.get_or_create(
                employee=employee,
                date=timezone.now().date(),
                defaults={'check_in': timezone.now().time()}
            )
            if not created:
                attendance.check_in = timezone.now().time()
                attendance.save()
            
            serializer = self.get_serializer(attendance)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def check_out(self, request):
        from django.utils import timezone
        
        employee_id = request.data.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
            attendance = EmployeeAttendance.objects.get(employee=employee, date=timezone.now().date())
            attendance.check_out = timezone.now().time()
            attendance.save()
            
            serializer = self.get_serializer(attendance)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except EmployeeAttendance.DoesNotExist:
            return Response({'error': 'No se encontró registro de entrada'}, status=status.HTTP_404_NOT_FOUND)


class EmployeeCommissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmployeeCommission.objects.all()
    serializer_class = EmployeeCommissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['employee__first_name', 'employee__last_name']
    filterset_fields = ['is_paid', 'employee']
    
    def get_queryset(self):
        return EmployeeCommission.objects.select_related('employee', 'sale')
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        commissions = self.get_queryset().filter(is_paid=False)
        serializer = self.get_serializer(commissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        commission = self.get_object()
        if commission.is_paid:
            return Response({'error': 'La comisión ya está pagada'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils import timezone
        commission.is_paid = True
        commission.paid_date = timezone.now().date()
        commission.save()
        
        serializer = self.get_serializer(commission)
        return Response(serializer.data)
