from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadOnlyOrAuthenticated(BasePermission):
    """
    Custom permission:
    - Read access (GET, HEAD, OPTIONS) is allowed for everyone.
    - Write access (POST, PUT, PATCH, DELETE) requires authentication.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
