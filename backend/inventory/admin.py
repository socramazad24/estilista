"""
Inventory admin for estilera project.
"""
from django.contrib import admin
from .models import ProductCategory, Product, InventoryMovement, InventoryCount, InventoryCountItem


class InventoryMovementInline(admin.TabularInline):
    model = InventoryMovement
    extra = 0
    readonly_fields = ['created_at']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'is_active']
    search_fields = ['name']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Productos'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'stock', 'min_stock', 'sale_price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'sku', 'barcode']
    inlines = [InventoryMovementInline]


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'previous_stock', 'new_stock', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__name', 'reference']


class InventoryCountItemInline(admin.TabularInline):
    model = InventoryCountItem
    extra = 0


@admin.register(InventoryCount)
class InventoryCountAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [InventoryCountItemInline]
