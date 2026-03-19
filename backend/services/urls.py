"""
Services URLs for estilera project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet, ServiceViewSet, ServicePackageViewSet

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet, basename='categories')
router.register(r'', ServiceViewSet, basename='services')
router.register(r'packages', ServicePackageViewSet, basename='packages')

urlpatterns = [
    path('', include(router.urls)),
]
