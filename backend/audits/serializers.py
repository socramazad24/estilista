"""
Audits serializers for estilera project.
"""
from rest_framework import serializers
from .models import AuditLog, SystemLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_name', 'action', 'action_display', 'model_name',
                  'object_id', 'object_repr', 'previous_data', 'new_data', 'ip_address',
                  'description', 'created_at']


class AuditLogSummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    total = serializers.IntegerField()
    create_count = serializers.IntegerField()
    update_count = serializers.IntegerField()
    delete_count = serializers.IntegerField()


class SystemLogSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = SystemLog
        fields = ['id', 'level', 'level_display', 'source', 'message', 'details', 'created_at']
