"""
Audit middleware for estilera project.
"""
import json
from .models import AuditLog


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Store request data before processing
        request.audit_data = {
            'method': request.method,
            'path': request.path,
            'user': request.user if request.user.is_authenticated else None,
        }
        
        response = self.get_response(request)
        
        # Log the request after processing
        self.log_request(request, response)
        
        return response
    
    def log_request(self, request, response):
        # Only log API requests
        if not request.path.startswith('/api/'):
            return
        
        # Skip token refresh and some read operations
        if request.path in ['/api/token/', '/api/token/refresh/']:
            return
        
        user = request.user if request.user.is_authenticated else None
        
        # Determine action based on method
        method_actions = {
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'PATCH': 'UPDATE',
            'DELETE': 'DELETE',
            'GET': 'VIEW',
        }
        action = method_actions.get(request.method, 'OTHER')
        
        # Extract model name from path
        path_parts = request.path.strip('/').split('/')
        model_name = path_parts[1] if len(path_parts) > 1 else 'unknown'
        
        # Get IP address
        ip_address = self.get_client_ip(request)
        
        # Create audit log
        try:
            AuditLog.objects.create(
                user=user,
                action=action,
                model_name=model_name,
                object_id='',
                object_repr='',
                previous_data=None,
                new_data=None,
                ip_address=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f"{request.method} {request.path} - Status: {response.status_code}"
            )
        except Exception:
            pass  # Don't break the request if logging fails
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
