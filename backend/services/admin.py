"""
Services admin for estilera project.
"""
from django.contrib import admin
from .models import ServiceCategory, Service, ServicePackage


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Servicios'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration_minutes', 'is_active', 'updated_at']
    list_filter = ['category', 'is_active', 'duration_minutes', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percentage', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['services']
