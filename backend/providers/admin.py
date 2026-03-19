"""
Providers admin for estilera project.
"""
from django.contrib import admin
from .models import Provider, ProviderContact, PurchaseOrder, PurchaseOrderItem


class ProviderContactInline(admin.TabularInline):
    model = ProviderContact
    extra = 1


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_name', 'phone', 'email', 'city', 'status']
    list_filter = ['status', 'city']
    search_fields = ['name', 'contact_name', 'nit']
    inlines = [ProviderContactInline]


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'provider', 'date', 'total', 'status']
    list_filter = ['status', 'date']
    search_fields = ['order_number', 'provider__name']
    inlines = [PurchaseOrderItemInline]
