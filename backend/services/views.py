"""
Services views for estilera project.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import ServiceCategory, Service, ServicePackage
from .serializers import (
    ServiceCategorySerializer, ServiceSerializer, 
    ServiceListSerializer, ServicePackageSerializer
)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        return ServiceCategory.objects.prefetch_related('services').all()
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        categories = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category', 'is_active', 'duration_minutes']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer
    
    def get_queryset(self):
        return Service.objects.select_related('category').all()
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        services = self.get_queryset().filter(is_active=True)
        serializer = ServiceListSerializer(services, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        categories = ServiceCategory.objects.filter(is_active=True)
        result = []
        for category in categories:
            services = Service.objects.filter(category=category, is_active=True)
            result.append({
                'category': ServiceCategorySerializer(category).data,
                'services': ServiceListSerializer(services, many=True).data
            })
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def top_services(self, request):
        from django.db.models import Count
        top_services = Service.objects.filter(
            is_active=True
        ).annotate(
            sale_count=Count('sale_items')
        ).order_by('-sale_count')[:10]
        serializer = ServiceListSerializer(top_services, many=True)
        return Response(serializer.data)


class ServicePackageViewSet(viewsets.ModelViewSet):
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        return ServicePackage.objects.prefetch_related('services').all()
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        packages = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(packages, many=True)
        return Response(serializer.data)
