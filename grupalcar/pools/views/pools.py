"""Pool views."""

# Django Rest Framework
from rest_framework import mixins, viewsets


# Permissions
from rest_framework.permissions import IsAuthenticated 
from grupalcar.pools.permissions.pools import IsPoolAdmin

# Serializers
from grupalcar.pools.serializers import PoolModelSerializer

# Models
from grupalcar.pools.models import Pool, Membership

class PoolViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Pool view set."""

    serializer_class = PoolModelSerializer

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Pool.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update','partial_update']:
            permissions.append(IsPoolAdmin)
        return [permission() for permission in permissions]

    def perform_create(self,serializer):
        """Assign pool admin."""
        pool = serializer.save()
        user = self.request.user
        profile = user.profile

        Membership.objects.create(
            user=user,
            profile=profile,
            pool=pool,
            is_admin=True,
            remaining_invitations=10
        )
        