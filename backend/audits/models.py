"""
Audits models for estilera project.
"""
from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cierre de sesión'),
        ('VIEW', 'Visualización'),
        ('EXPORT', 'Exportación'),
        ('PRINT', 'Impresión'),
        ('OTHER', 'Otro'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                             null=True, blank=True, related_name='audit_logs', verbose_name='Usuario')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='Acción')
    model_name = models.CharField(max_length=100, verbose_name='Modelo')
    object_id = models.CharField(max_length=100, blank=True, verbose_name='ID del objeto')
    object_repr = models.CharField(max_length=255, blank=True, verbose_name='Representación del objeto')
    previous_data = models.JSONField(null=True, blank=True, verbose_name='Datos anteriores')
    new_data = models.JSONField(null=True, blank=True, verbose_name='Datos nuevos')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    description = models.TextField(blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Registro de auditoría'
        verbose_name_plural = 'Registros de auditoría'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.model_name} - {self.created_at}"


class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'Información'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
        ('DEBUG', 'Debug'),
        ('CRITICAL', 'Crítico'),
    ]
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='INFO', verbose_name='Nivel')
    source = models.CharField(max_length=100, verbose_name='Fuente')
    message = models.TextField(verbose_name='Mensaje')
    details = models.JSONField(null=True, blank=True, verbose_name='Detalles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Log del sistema'
        verbose_name_plural = 'Logs del sistema'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_level_display()} - {self.source} - {self.created_at}"
