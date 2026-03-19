"""
Users models for estilera project.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('stylist', 'Estilista'),
        ('cashier', 'Cajero'),
        ('assistant', 'Asistente'),
    ]
    
    username = models.CharField(max_length=150, unique=True, verbose_name='Usuario')
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    first_name = models.CharField(max_length=150, verbose_name='Nombres')
    last_name = models.CharField(max_length=150, verbose_name='Apellidos')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='assistant', verbose_name='Rol')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Fecha de registro')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Último acceso')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', verbose_name='Usuario')
    action = models.CharField(max_length=100, verbose_name='Acción')
    description = models.TextField(blank=True, verbose_name='Descripción')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Actividad de usuario'
        verbose_name_plural = 'Actividades de usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.created_at}"
