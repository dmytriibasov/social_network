from rest_framework.permissions import BasePermission, SAFE_METHODS


class NotAuthenticated(BasePermission):
    """
    Simple permission class to check if user isn't authenticated. (To avoid signup flow if user is logged in)
    """
    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)


class IsCurrentUserOrReadOnly(BasePermission):
    """
    Permission class to grant only the current user change its data
    """
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj == request.user
