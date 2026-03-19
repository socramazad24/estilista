"""
Inventory URLs for estilera project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductViewSet, InventoryMovementViewSet, InventoryCountViewSet

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet, basename='product-categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'movements', InventoryMovementViewSet, basename='movements')
router.register(r'counts', InventoryCountViewSet, basename='counts')

urlpatterns = [
    path('', include(router.urls)),
]
