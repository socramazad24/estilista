"""
Audits admin for estilera project.
"""
from django.contrib import admin
from .models import AuditLog, SystemLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'action', 'model_name', 'user', 'ip_address']
    list_filter = ['action', 'model_name', 'created_at']
    search_fields = ['model_name', 'object_repr', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'level', 'source', 'message']
    list_filter = ['level', 'created_at']
    search_fields = ['source', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
