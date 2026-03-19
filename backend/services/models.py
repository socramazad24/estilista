"""
Services models for estilera project.
"""
from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    color = models.CharField(max_length=7, default='#3B82F6', verbose_name='Color')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Categoría de servicio'
        verbose_name_plural = 'Categorías de servicios'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Service(models.Model):
    DURATION_CHOICES = [
        (15, '15 minutos'),
        (30, '30 minutos'),
        (45, '45 minutos'),
        (60, '1 hora'),
        (90, '1 hora 30 min'),
        (120, '2 horas'),
        (150, '2 horas 30 min'),
        (180, '3 horas'),
    ]
    
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='services', verbose_name='Categoría')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio')
    duration_minutes = models.IntegerField(choices=DURATION_CHOICES, default=60, verbose_name='Duración')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - ${self.price:,.0f}"
    
    def get_duration_display_short(self):
        duration_map = {
            15: '15m',
            30: '30m',
            45: '45m',
            60: '1h',
            90: '1h30m',
            120: '2h',
            150: '2h30m',
            180: '3h',
        }
        return duration_map.get(self.duration_minutes, f"{self.duration_minutes}m")


class ServicePackage(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    services = models.ManyToManyField(Service, related_name='packages', verbose_name='Servicios')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Descuento %')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Paquete de servicios'
        verbose_name_plural = 'Paquetes de servicios'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_total_price(self):
        total = sum(service.price for service in self.services.all())
        discount = total * (self.discount_percentage / 100)
        return total - discount
