"""Pools permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from grupalcar.pools.models import Membership

class IsPoolAdmin(BasePermission):
    """Allow access only to pool admins."""

    def has_object_permission(self, request, view, obj):
        """Verify user have a membership and is admin in the Pool obj."""
        try:
            Membership.objects.get(
                user=request.user,
                pool=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
    