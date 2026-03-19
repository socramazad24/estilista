"""
Providers URLs for estilera project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProviderViewSet, ProviderContactViewSet, PurchaseOrderViewSet

router = DefaultRouter()
router.register(r'', ProviderViewSet, basename='providers')
router.register(r'contacts', ProviderContactViewSet, basename='contacts')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-orders')

urlpatterns = [
    path('', include(router.urls)),
]
