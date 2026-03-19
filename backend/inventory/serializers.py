"""
Inventory serializers for estilera project.
"""
from rest_framework import serializers
from .models import ProductCategory, Product, InventoryMovement, InventoryCount, InventoryCountItem


class ProductCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description', 'is_active', 'product_count', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    unit_display = serializers.CharField(source='get_unit_display', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'category_name', 'provider', 'provider_name', 'name', 
                  'description', 'sku', 'barcode', 'unit', 'unit_display', 'stock', 
                  'min_stock', 'max_stock', 'purchase_price', 'sale_price', 'location',
                  'is_low_stock', 'is_active', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'category_name', 'stock', 'min_stock', 
                  'is_low_stock', 'sale_price', 'is_active']


class InventoryMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = InventoryMovement
        fields = ['id', 'product', 'product_name', 'product_sku', 'movement_type',
                  'movement_type_display', 'quantity', 'previous_stock', 'new_stock',
                  'unit_price', 'total_price', 'reference', 'notes', 
                  'created_by', 'created_by_name', 'created_at']


class InventoryMovementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = ['product', 'movement_type', 'quantity', 'unit_price', 'reference', 'notes']
    
    def create(self, validated_data):
        product = validated_data['product']
        movement_type = validated_data['movement_type']
        quantity = validated_data['quantity']
        
        previous_stock = product.stock
        
        if movement_type == 'entry':
            product.stock += quantity
        elif movement_type == 'exit':
            product.stock -= quantity
        elif movement_type == 'return':
            product.stock += quantity
        elif movement_type == 'adjustment':
            product.stock = quantity
        
        product.save()
        
        validated_data['previous_stock'] = previous_stock
        validated_data['new_stock'] = product.stock
        validated_data['created_by'] = self.context['request'].user
        
        return super().create(validated_data)


class InventoryCountItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    
    class Meta:
        model = InventoryCountItem
        fields = ['id', 'product', 'product_name', 'product_sku', 'expected_quantity',
                  'counted_quantity', 'difference', 'notes']


class InventoryCountSerializer(serializers.ModelSerializer):
    items = InventoryCountItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    completed_by_name = serializers.CharField(source='completed_by.get_full_name', read_only=True)
    
    class Meta:
        model = InventoryCount
        fields = ['id', 'name', 'description', 'status', 'status_display', 'items',
                  'started_at', 'completed_at', 'created_by', 'created_by_name',
                  'completed_by', 'completed_by_name', 'created_at']


class InventoryCountCreateSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    
    class Meta:
        model = InventoryCount
        fields = ['name', 'description', 'product_ids']
    
    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids')
        validated_data['created_by'] = self.context['request'].user
        inventory_count = super().create(validated_data)
        
        from .models import Product
        for product in Product.objects.filter(id__in=product_ids):
            InventoryCountItem.objects.create(
                inventory_count=inventory_count,
                product=product,
                expected_quantity=product.stock
            )
        
        return inventory_count
