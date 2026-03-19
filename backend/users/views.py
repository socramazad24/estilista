"""
Users views for estilera project.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, UserActivity
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserActivitySerializer, ChangePasswordSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    filterset_fields = ['role', 'is_active']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': ['Contraseña actual incorrecta']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Contraseña actualizada correctamente'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def stylists(self, request):
        stylists = User.objects.filter(role__in=['stylist', 'admin'], is_active=True)
        serializer = self.get_serializer(stylists, many=True)
        return Response(serializer.data)


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['action', 'description']
    filterset_fields = ['user']
    
    def get_queryset(self):
        queryset = UserActivity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.order_by('-created_at')
