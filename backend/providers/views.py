"""
Providers views for estilera project.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Provider, ProviderContact, PurchaseOrder
from .serializers import (
    ProviderSerializer, ProviderListSerializer, ProviderContactSerializer,
    PurchaseOrderSerializer, PurchaseOrderCreateSerializer
)


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'contact_name', 'phone', 'email', 'nit']
    filterset_fields = ['status', 'city']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProviderListSerializer
        return ProviderSerializer
    
    def get_queryset(self):
        return Provider.objects.prefetch_related('contacts')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        providers = self.get_queryset().filter(status='active')
        serializer = ProviderListSerializer(providers, many=True)
        return Response(serializer.data)


class ProviderContactViewSet(viewsets.ModelViewSet):
    queryset = ProviderContact.objects.all()
    serializer_class = ProviderContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'position', 'email']
    
    def get_queryset(self):
        return ProviderContact.objects.select_related('provider')


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['order_number', 'provider__name']
    filterset_fields = ['status', 'provider']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PurchaseOrderCreateSerializer
        return PurchaseOrderSerializer
    
    def get_queryset(self):
        return PurchaseOrder.objects.select_related('provider').prefetch_related('items')
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        purchase_order = self.get_object()
        if purchase_order.status != 'draft':
            return Response({'error': 'La orden ya fue enviada'}, status=status.HTTP_400_BAD_REQUEST)
        
        purchase_order.status = 'sent'
        purchase_order.save()
        
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        purchase_order = self.get_object()
        if purchase_order.status != 'sent':
            return Response({'error': 'La orden debe estar enviada para recibirla'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update inventory
        from inventory.models import Product, InventoryMovement
        for item in purchase_order.items.all():
            # Try to find product by name
            try:
                product = Product.objects.filter(name__iexact=item.product_name).first()
                if product:
                    previous_stock = product.stock
                    product.stock += item.quantity
                    product.save()
                    
                    InventoryMovement.objects.create(
                        product=product,
                        movement_type='entry',
                        quantity=item.quantity,
                        previous_stock=previous_stock,
                        new_stock=product.stock,
                        unit_price=item.unit_price,
                        reference=f"OC #{purchase_order.order_number}",
                        notes=f"Recepción de orden de compra",
                        created_by=request.user
                    )
            except Product.DoesNotExist:
                pass
        
        purchase_order.status = 'received'
        purchase_order.save()
        
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        purchase_order = self.get_object()
        if purchase_order.status == 'received':
            return Response({'error': 'No se puede cancelar una orden recibida'}, status=status.HTTP_400_BAD_REQUEST)
        
        purchase_order.status = 'cancelled'
        purchase_order.save()
        
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)
