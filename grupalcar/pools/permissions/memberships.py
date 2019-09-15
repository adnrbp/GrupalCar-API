"""Pool permission classes."""

# Django Rest Framework
from rest_framework.permissions import BasePermission

# Models
from grupalcar.pools.models import Membership

class IsActivePoolMember(BasePermission):
    """Allow access only to pool members.

    Expect that views implementing this permission
    have a 'Pool' attribute assigned
    """

    def has_permission(self,request,view):
        """Verify user is an active member of the pool."""
        try:
            Membership.objects.get(
                user=request.user,
                pool=view.pool,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True

class IsSelfMember(BasePermission):
    """Allow access only to member owners."""

    def has_permission(self, request, view):
        """Let object permission grant access."""
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Allow access only if member is owned by the requesting user."""
        return request.user == obj.user