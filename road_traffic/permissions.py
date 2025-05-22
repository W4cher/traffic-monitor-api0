from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.info(f"Checking permission for {request.method}")
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    
#part3
class HasSensorAPIKey(permissions.BasePermission):
    VALID_API_KEY = "23231c7a-80a7-4810-93b3-98a18ecfbc42" 

    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-Key')
        logger.info(f"Checking API Key: {api_key}")
        if api_key == self.VALID_API_KEY:
            return True
        logger.warning("Invalid or missing API Key")
        return False