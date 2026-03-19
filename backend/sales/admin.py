"""
Sales admin for estilera project.
"""
from django.contrib import admin
from .models import Client, Sale, SaleItem, DailyCashRegister


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['total']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'phone', 'email', 'sales_count', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    
    def sales_count(self, obj):
        return obj.sales.count()
    sales_count.short_description = 'Compras'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'client', 'stylist', 'total', 'payment_method', 'status', 'date']
    list_filter = ['status', 'payment_method', 'date']
    search_fields = ['invoice_number', 'client__first_name', 'client__last_name']
    inlines = [SaleItemInline]
    readonly_fields = ['invoice_number', 'date', 'created_at']


@admin.register(DailyCashRegister)
class DailyCashRegisterAdmin(admin.ModelAdmin):
    list_display = ['date', 'opening_amount', 'closing_amount', 'total_sales', 'status']
    list_filter = ['status', 'date']
    readonly_fields = ['opened_at', 'closed_at']
