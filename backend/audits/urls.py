"""
Audits URLs for estilera project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet, SystemLogViewSet

router = DefaultRouter()
router.register(r'logs', AuditLogViewSet, basename='audit-logs')
router.register(r'system-logs', SystemLogViewSet, basename='system-logs')

urlpatterns = [
    path('', include(router.urls)),
]
