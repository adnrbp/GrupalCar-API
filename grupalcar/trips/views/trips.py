"""Trip views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from grupalcar.pools.permissions.memberships import IsActivePoolMember

# Serializers
from grupalcar.trips.serializers import CreateTripSerializer

# Models
from grupalcar.pools.models import Pool


class TripViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = CreateTripSerializer
    permission_classes = [IsAuthenticated, IsActivePoolMember]

    def dispatch(self,request, *args, **kwargs):
        """Verify that the pool exists."""
        slug_name = kwargs['slug_name']
        self.pool = get_object_or_404(
            Pool,
            slug_name=slug_name
        )
        return super(TripViewSet,self).dispatch(request, *args, **kwargs)
    
    def get_serializer_context(self):
        """Add pool to serializer context."""
        context = super(TripViewSet, self).get_serializer_context()
        context['pool'] = self.pool
        return context