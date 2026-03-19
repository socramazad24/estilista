"""
Inventory views for estilera project.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import ProductCategory, Product, InventoryMovement, InventoryCount
from .serializers import (
    ProductCategorySerializer, ProductSerializer, ProductListSerializer,
    InventoryMovementSerializer, InventoryMovementCreateSerializer,
    InventoryCountSerializer, InventoryCountCreateSerializer
)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'sku', 'barcode', 'description']
    filterset_fields = ['category', 'provider', 'is_active']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    def get_queryset(self):
        return Product.objects.select_related('category', 'provider')
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        products = self.get_queryset().filter(stock__lte=models.F('min_stock'), is_active=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        products = self.get_queryset().filter(is_active=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['product__name', 'reference', 'notes']
    filterset_fields = ['movement_type', 'product']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InventoryMovementCreateSerializer
        return InventoryMovementSerializer
    
    def get_queryset(self):
        return InventoryMovement.objects.select_related('product', 'created_by')
    
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'product_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        movements = self.get_queryset().filter(product_id=product_id)[:50]
        serializer = self.get_serializer(movements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        movements = self.get_queryset()[:20]
        serializer = self.get_serializer(movements, many=True)
        return Response(serializer.data)


class InventoryCountViewSet(viewsets.ModelViewSet):
    queryset = InventoryCount.objects.all()
    serializer_class = InventoryCountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InventoryCountCreateSerializer
        return InventoryCountSerializer
    
    def get_queryset(self):
        return InventoryCount.objects.select_related('created_by', 'completed_by').prefetch_related('items', 'items__product')
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        inventory_count = self.get_object()
        if inventory_count.status != 'pending':
            return Response({'error': 'El conteo ya fue iniciado'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils import timezone
        inventory_count.status = 'in_progress'
        inventory_count.started_at = timezone.now()
        inventory_count.save()
        
        serializer = self.get_serializer(inventory_count)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        inventory_count = self.get_object()
        if inventory_count.status != 'in_progress':
            return Response({'error': 'El conteo no está en progreso'}, status=status.HTTP_400_BAD_REQUEST)
        
        items_data = request.data.get('items', [])
        from .models import InventoryCountItem
        
        for item_data in items_data:
            item_id = item_data.get('id')
            counted_quantity = item_data.get('counted_quantity')
            notes = item_data.get('notes', '')
            
            try:
                item = InventoryCountItem.objects.get(id=item_id, inventory_count=inventory_count)
                item.counted_quantity = counted_quantity
                item.notes = notes
                item.save()
                
                # Update product stock if there's a difference
                if item.difference != 0:
                    product = item.product
                    product.stock = item.counted_quantity
                    product.save()
                    
                    # Create inventory movement
                    InventoryMovement.objects.create(
                        product=product,
                        movement_type='adjustment',
                        quantity=item.counted_quantity,
                        previous_stock=item.expected_quantity,
                        new_stock=item.counted_quantity,
                        reference=f"Conteo #{inventory_count.id}",
                        notes=f"Ajuste por conteo: {notes}",
                        created_by=request.user
                    )
            except InventoryCountItem.DoesNotExist:
                continue
        
        from django.utils import timezone
        inventory_count.status = 'completed'
        inventory_count.completed_at = timezone.now()
        inventory_count.completed_by = request.user
        inventory_count.save()
        
        serializer = self.get_serializer(inventory_count)
        return Response(serializer.data)
