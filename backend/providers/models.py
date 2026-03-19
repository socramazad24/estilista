"""
Providers models for estilera project.
"""
from django.db import models


class Provider(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
    ]
    
    name = models.CharField(max_length=150, verbose_name='Nombre')
    contact_name = models.CharField(max_length=150, blank=True, verbose_name='Nombre de contacto')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    address = models.TextField(blank=True, verbose_name='Dirección')
    city = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    nit = models.CharField(max_length=20, blank=True, verbose_name='NIT')
    website = models.URLField(blank=True, verbose_name='Sitio web')
    notes = models.TextField(blank=True, verbose_name='Notas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProviderContact(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='contacts', verbose_name='Proveedor')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    position = models.CharField(max_length=100, blank=True, verbose_name='Cargo')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    is_primary = models.BooleanField(default=False, verbose_name='Contacto principal')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    
    class Meta:
        verbose_name = 'Contacto de proveedor'
        verbose_name_plural = 'Contactos de proveedores'
        ordering = ['-is_primary', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.provider.name}"


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('sent', 'Enviada'),
        ('received', 'Recibida'),
        ('cancelled', 'Cancelada'),
    ]
    
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name='purchase_orders', verbose_name='Proveedor')
    order_number = models.CharField(max_length=20, unique=True, verbose_name='Número de orden')
    date = models.DateField(verbose_name='Fecha')
    expected_date = models.DateField(null=True, blank=True, verbose_name='Fecha esperada')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Subtotal')
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Impuesto')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Estado')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Órdenes de compra'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Orden #{self.order_number} - {self.provider.name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        from datetime import datetime
        prefix = 'OC'
        date_str = datetime.now().strftime('%Y%m%d')
        last_order = PurchaseOrder.objects.filter(order_number__startswith=f"{prefix}{date_str}").order_by('-id').first()
        if last_order:
            last_number = int(last_order.order_number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f"{prefix}{date_str}{new_number:04d}"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items', verbose_name='Orden de compra')
    product_name = models.CharField(max_length=150, verbose_name='Nombre del producto')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cantidad')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio unitario')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total')
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Item de orden de compra'
        verbose_name_plural = 'Items de orden de compra'
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
