"""
Sales URLs for estilera project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, SaleViewSet, DailyCashRegisterViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'', SaleViewSet, basename='sales')
router.register(r'cash-register', DailyCashRegisterViewSet, basename='cash-register')

urlpatterns = [
    path('', include(router.urls)),
]
