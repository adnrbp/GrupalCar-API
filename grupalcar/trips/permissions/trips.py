"""Trips permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

class IsPoolOwner(BasePermission):
    """Verify requesting user is the trip creator."""

    def has_object_permission(self, request, view, obj):
        """Verify user as trip creator."""
        return request.user == obj.offered_by