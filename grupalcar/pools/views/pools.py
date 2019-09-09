"""Pool views."""

# Django Rest Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from grupalcar.pools.serializers import PoolModelSerializer

# Models
from grupalcar.pools.models import Pool, Membership

class PoolViewSet(viewsets.ModelViewSet):
    """Pool view set."""

    serializer_class = PoolModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Pool.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

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
        