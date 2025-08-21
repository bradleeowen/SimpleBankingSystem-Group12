from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsReadOnlyOrAuthenticated(BasePermission):
    """
    Custom permission:
    - Read-only (GET, HEAD, OPTIONS) allowed for everyone.
    - Write permissions (POST, PUT, PATCH, DELETE) only for authenticated users.
    """

    def has_permission(self, request, view):
        # Allow all safe (read-only) methods for everyone
        if request.method in SAFE_METHODS:
            return True
        
        # For unsafe (write) methods, user must be authenticated
        return request.user and request.user.is_authenticated

