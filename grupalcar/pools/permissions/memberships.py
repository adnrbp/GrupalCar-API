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