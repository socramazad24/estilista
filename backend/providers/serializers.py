"""
Providers serializers for estilera project.
"""
from rest_framework import serializers
from .models import Provider, ProviderContact, PurchaseOrder, PurchaseOrderItem


class ProviderContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderContact
        fields = ['id', 'name', 'position', 'phone', 'email', 'is_primary', 'created_at']


class ProviderSerializer(serializers.ModelSerializer):
    contacts = ProviderContactSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Provider
        fields = ['id', 'name', 'contact_name', 'phone', 'email', 'address', 
                  'city', 'nit', 'website', 'notes', 'status', 'status_display',
                  'contacts', 'created_at', 'updated_at']


class ProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'phone', 'email', 'city', 'status']


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'product_name', 'quantity', 'unit_price', 'total', 'notes']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'provider', 'provider_name', 'order_number', 'date', 
                  'expected_date', 'subtotal', 'tax', 'total', 'status', 
                  'status_display', 'items', 'notes', 'created_at', 'updated_at']


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['provider', 'date', 'expected_date', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        
        subtotal = 0
        for item_data in items_data:
            item = PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)
            subtotal += item.total
        
        purchase_order.subtotal = subtotal
        purchase_order.tax = subtotal * 0.19  # 19% IVA
        purchase_order.total = purchase_order.subtotal + purchase_order.tax
        purchase_order.save()
        
        return purchase_order
