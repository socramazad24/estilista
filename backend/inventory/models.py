"""
Inventory models for estilera project.
"""
from django.db import models
from django.conf import settings
from providers.models import Provider


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        verbose_name = 'Categoría de producto'
        verbose_name_plural = 'Categorías de productos'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('unit', 'Unidad'),
        ('ml', 'Mililitros'),
        ('l', 'Litros'),
        ('g', 'Gramos'),
        ('kg', 'Kilogramos'),
        ('oz', 'Onzas'),
        ('box', 'Caja'),
        ('bottle', 'Botella'),
    ]
    
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products', verbose_name='Categoría')
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='Proveedor')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    sku = models.CharField(max_length=50, unique=True, blank=True, verbose_name='Código SKU')
    barcode = models.CharField(max_length=50, blank=True, verbose_name='Código de barras')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='unit', verbose_name='Unidad')
    stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Stock actual')
    min_stock = models.DecimalField(max_digits=12, decimal_places=2, default=5, verbose_name='Stock mínimo')
    max_stock = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Stock máximo')
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio de compra')
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio de venta')
    location = models.CharField(max_length=100, blank=True, verbose_name='Ubicación')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.sku}) - Stock: {self.stock}"
    
    def is_low_stock(self):
        return self.stock <= self.min_stock
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_sku()
        super().save(*args, **kwargs)
    
    def generate_sku(self):
        prefix = 'PROD'
        last_product = Product.objects.filter(sku__startswith=prefix).order_by('-id').first()
        if last_product:
            last_number = int(last_product.sku.replace(prefix, ''))
            new_number = last_number + 1
        else:
            new_number = 1
        return f"{prefix}{new_number:06d}"


class InventoryMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('entry', 'Entrada'),
        ('exit', 'Salida'),
        ('adjustment', 'Ajuste'),
        ('return', 'Devolución'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name='Producto')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, verbose_name='Tipo de movimiento')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cantidad')
    previous_stock = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Stock anterior')
    new_stock = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Stock nuevo')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio unitario')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio total')
    reference = models.CharField(max_length=100, blank=True, verbose_name='Referencia')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Movimiento de inventario'
        verbose_name_plural = 'Movimientos de inventario'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class InventoryCount(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]
    
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de inicio')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_counts', verbose_name='Creado por')
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='completed_counts', verbose_name='Completado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        verbose_name = 'Conteo de inventario'
        verbose_name_plural = 'Conteos de inventario'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class InventoryCountItem(models.Model):
    inventory_count = models.ForeignKey(InventoryCount, on_delete=models.CASCADE, related_name='items', verbose_name='Conteo')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    expected_quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cantidad esperada')
    counted_quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Cantidad contada')
    difference = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Diferencia')
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Item de conteo'
        verbose_name_plural = 'Items de conteo'
    
    def __str__(self):
        return f"{self.product.name} - Esperado: {self.expected_quantity}, Contado: {self.counted_quantity}"
    
    def save(self, *args, **kwargs):
        if self.counted_quantity is not None:
            self.difference = self.counted_quantity - self.expected_quantity
        super().save(*args, **kwargs)
