"""
Services serializers for estilera project.
"""
from rest_framework import serializers
from .models import ServiceCategory, Service, ServicePackage


class ServiceCategorySerializer(serializers.ModelSerializer):
    service_count = serializers.IntegerField(source='services.count', read_only=True)
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'color', 'is_active', 'service_count', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    duration_short = serializers.CharField(source='get_duration_display_short', read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'category', 'category_name', 'category_color', 'name', 'description', 
                  'price', 'duration_minutes', 'duration_display', 'duration_short',
                  'is_active', 'created_at', 'updated_at']


class ServiceListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    duration_short = serializers.CharField(source='get_duration_display_short', read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'category', 'category_name', 'category_color', 'name', 'price', 'duration_short', 'is_active']


class ServicePackageSerializer(serializers.ModelSerializer):
    services_detail = ServiceListSerializer(source='services', many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = ServicePackage
        fields = ['id', 'name', 'description', 'services', 'services_detail', 
                  'discount_percentage', 'total_price', 'is_active', 'created_at', 'updated_at']
