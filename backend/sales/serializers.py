"""
Sales serializers for estilera project.
"""
from rest_framework import serializers
from .models import Client, Sale, SaleItem, DailyCashRegister
from services.serializers import ServiceListSerializer


class ClientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    sales_count = serializers.IntegerField(source='sales.count', read_only=True)
    total_spent = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'full_name', 'phone', 'email', 
                  'address', 'notes', 'sales_count', 'total_spent', 'created_at', 'updated_at']
    
    def get_total_spent(self, obj):
        return sum(sale.total for sale in obj.sales.filter(status='completed'))


class ClientListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'full_name', 'phone', 'email']


class SaleItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_detail = ServiceListSerializer(source='service', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = ['id', 'service', 'service_name', 'service_detail', 'quantity', 
                  'unit_price', 'discount', 'total', 'notes']


class SaleItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['service', 'quantity', 'unit_price', 'discount', 'notes']


class SaleSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    stylist_name = serializers.CharField(source='stylist.get_full_name', read_only=True)
    cashier_name = serializers.CharField(source='cashier.get_full_name', read_only=True)
    items = SaleItemSerializer(many=True, read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'invoice_number', 'client', 'client_name', 'stylist', 'stylist_name',
                  'cashier', 'cashier_name', 'date', 'items', 'subtotal', 'discount', 
                  'tax', 'total', 'payment_method', 'payment_method_display', 
                  'status', 'status_display', 'notes', 'created_at']


class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemCreateSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ['client', 'stylist', 'subtotal', 'discount', 'tax', 'total', 
                  'payment_method', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['cashier'] = self.context['request'].user
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            SaleItem.objects.create(sale=sale, **item_data)
        
        return sale


class SaleListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    item_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'invoice_number', 'client_name', 'total', 'payment_method', 
                  'status', 'date', 'item_count']


class DailyCashRegisterSerializer(serializers.ModelSerializer):
    opened_by_name = serializers.CharField(source='opened_by.get_full_name', read_only=True)
    closed_by_name = serializers.CharField(source='closed_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    difference = serializers.SerializerMethodField()
    
    class Meta:
        model = DailyCashRegister
        fields = ['id', 'date', 'opening_amount', 'closing_amount', 'total_sales',
                  'total_cash', 'total_card', 'total_transfer', 'total_other',
                  'opened_by', 'opened_by_name', 'closed_by', 'closed_by_name',
                  'status', 'status_display', 'notes', 'opened_at', 'closed_at', 'difference']
    
    def get_difference(self, obj):
        if obj.closing_amount:
            expected = obj.opening_amount + obj.total_cash
            return obj.closing_amount - expected
        return None


class SalesReportSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_sale = serializers.DecimalField(max_digits=12, decimal_places=2)
    by_payment_method = serializers.DictField()
    by_service = serializers.ListField()
