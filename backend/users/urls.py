"""
Users URLs for estilera project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserActivityViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')
router.register(r'activities', UserActivityViewSet, basename='activities')

urlpatterns = [
    path('', include(router.urls)),
]
