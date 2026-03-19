"""
Sales models for estilera project.
"""
from django.db import models
from django.conf import settings
from services.models import Service, ServicePackage


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Nombres')
    last_name = models.CharField(max_length=150, verbose_name='Apellidos')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    address = models.TextField(blank=True, verbose_name='Dirección')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Sale(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
        ('nequi', 'Nequi'),
        ('daviplata', 'Daviplata'),
        ('other', 'Otro'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name='Número de factura')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='sales', verbose_name='Cliente')
    stylist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
                                related_name='sales_as_stylist', verbose_name='Estilista')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
                                related_name='sales_as_cashier', verbose_name='Cajero')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Subtotal')
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Descuento')
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Impuesto')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', verbose_name='Método de pago')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='Estado')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Factura {self.invoice_number} - {self.client} - ${self.total:,.0f}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        from datetime import datetime
        prefix = 'EST'
        date_str = datetime.now().strftime('%Y%m%d')
        last_sale = Sale.objects.filter(invoice_number__startswith=f"{prefix}{date_str}").order_by('-id').first()
        if last_sale:
            last_number = int(last_sale.invoice_number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f"{prefix}{date_str}{new_number:04d}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name='Venta')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='sale_items', verbose_name='Servicio')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio unitario')
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Descuento')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total')
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Item de venta'
        verbose_name_plural = 'Items de venta'
    
    def __str__(self):
        return f"{self.service.name} x{self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total = (self.unit_price * self.quantity) - self.discount
        super().save(*args, **kwargs)


class DailyCashRegister(models.Model):
    STATUS_CHOICES = [
        ('open', 'Abierta'),
        ('closed', 'Cerrada'),
    ]
    
    date = models.DateField(unique=True, verbose_name='Fecha')
    opening_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto de apertura')
    closing_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Monto de cierre')
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total ventas')
    total_cash = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total efectivo')
    total_card = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total tarjeta')
    total_transfer = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total transferencias')
    total_other = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total otros')
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
                                  related_name='opened_cash_registers', verbose_name='Abierto por')
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
                                  related_name='closed_cash_registers', verbose_name='Cerrado por')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='Estado')
    notes = models.TextField(blank=True, verbose_name='Notas')
    opened_at = models.DateTimeField(auto_now_add=True, verbose_name='Hora de apertura')
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name='Hora de cierre')
    
    class Meta:
        verbose_name = 'Caja diaria'
        verbose_name_plural = 'Cajas diarias'
        ordering = ['-date']
    
    def __str__(self):
        return f"Caja {self.date} - {self.get_status_display()}"
