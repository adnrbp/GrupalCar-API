"""Pool membership views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Serializers
from grupalcar.pools.serializers import MembershipModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from grupalcar.pools.permissions.memberships import IsActivePoolMember

# Models
from grupalcar.pools.models import Pool, Membership

class MembershipViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Pool membership view set."""

    serializer_class = MembershipModelSerializer

    def dispatch(self,request,*args,**kwargs):
        """Verify that the pool exists."""
        slug_name = kwargs['slug_name']
        self.pool = get_object_or_404(
            Pool,
            slug_name=slug_name
        )
        return super(MembershipViewSet,self).dispatch(request, *args, **kwargs)
    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsActivePoolMember]
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Return pool members."""
        return Membership.objects.filter(
            pool=self.pool,
            is_active=True
        )