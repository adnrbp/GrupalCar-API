"""Trips permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

class IsTripOwner(BasePermission):
    """Verify requesting user is the trip creator."""

    def has_object_permission(self, request, view, obj):
        """Verify user as trip creator."""
        return request.user == obj.offered_by

class IsNotTripOwner(BasePermission):
    """Only users that are not trip owners can call the view."""

    def has_object_permission(self, request, view, obj):
        """Verify user is not the trip creator."""
        return not request.user == obj.offered_by