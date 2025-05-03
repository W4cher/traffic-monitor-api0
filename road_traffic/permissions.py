from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        logger.info(f"Checking IsAdminOrReadOnly for method {request.method} by user {request.user}")
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        is_staff = request.user and request.user.is_staff
        logger.info(f"User is staff: {is_staff}")
        return is_staff