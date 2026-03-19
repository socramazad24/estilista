"""
Audits views for estilera project.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import AuditLog, SystemLog
from .serializers import AuditLogSerializer, SystemLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['model_name', 'object_repr', 'description', 'user__first_name', 'user__last_name']
    filterset_fields = ['action', 'model_name', 'user']
    
    def get_queryset(self):
        return AuditLog.objects.select_related('user')
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        logs = self.get_queryset()[:50]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_model(self, request):
        model_name = request.query_params.get('model_name')
        if not model_name:
            return Response({'error': 'model_name es requerido'}, status=400)
        
        logs = self.get_queryset().filter(model_name=model_name)[:100]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id es requerido'}, status=400)
        
        logs = self.get_queryset().filter(user_id=user_id)[:100]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        logs = AuditLog.objects.filter(created_at__gte=start_date)
        
        # Summary by action
        by_action = logs.values('action').annotate(count=Count('id'))
        by_action_dict = {item['action']: item['count'] for item in by_action}
        
        # Summary by model
        by_model = logs.values('model_name').annotate(count=Count('id')).order_by('-count')[:10]
        
        # Summary by user
        by_user = logs.values('user__first_name', 'user__last_name').annotate(count=Count('id')).order_by('-count')[:10]
        
        # Daily summary
        daily = []
        for i in range(days):
            date = (timezone.now() - timedelta(days=i)).date()
            day_logs = logs.filter(created_at__date=date)
            daily.append({
                'date': date,
                'total': day_logs.count(),
                'create_count': day_logs.filter(action='CREATE').count(),
                'update_count': day_logs.filter(action='UPDATE').count(),
                'delete_count': day_logs.filter(action='DELETE').count(),
            })
        
        return Response({
            'period_days': days,
            'total_logs': logs.count(),
            'by_action': by_action_dict,
            'by_model': list(by_model),
            'by_user': list(by_user),
            'daily': daily
        })
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        today = timezone.now().date()
        
        # Today's activity
        today_logs = AuditLog.objects.filter(created_at__date=today)
        today_count = today_logs.count()
        
        # Most active users today
        active_users = today_logs.values('user__first_name', 'user__last_name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Most affected models today
        active_models = today_logs.values('model_name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Recent actions
        recent_logs = self.get_queryset()[:10]
        recent_serializer = self.get_serializer(recent_logs, many=True)
        
        return Response({
            'today_count': today_count,
            'active_users': list(active_users),
            'active_models': list(active_models),
            'recent_actions': recent_serializer.data
        })


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['source', 'message']
    filterset_fields = ['level', 'source']
    
    @action(detail=False, methods=['get'])
    def errors(self, request):
        logs = SystemLog.objects.filter(level__in=['ERROR', 'CRITICAL']).order_by('-created_at')[:50]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        logs = SystemLog.objects.order_by('-created_at')[:50]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
