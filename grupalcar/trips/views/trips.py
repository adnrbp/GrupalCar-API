"""Trip views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from grupalcar.pools.permissions.memberships import IsActivePoolMember
from grupalcar.trips.permissions.trips import IsPoolOwner

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Serializers
from grupalcar.trips.serializers import (
    CreateTripSerializer,
    TripModelSerializer
)

# Models
from grupalcar.pools.models import Pool

# Utilities
from datetime import timedelta
from django.utils import timezone

class TripViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    filter_backends = (SearchFilter, OrderingFilter)

    ordering = ('departure_date','arrival_date','available_seats')
    ordering_fields = ('departure_date','arrival_date','available_seats')
    search_fields = ('departure_location','arrival_location')

    def dispatch(self,request, *args, **kwargs):
        """Verify that the pool exists."""
        slug_name = kwargs['slug_name']
        self.pool = get_object_or_404(
            Pool,
            slug_name=slug_name
        )
        return super(TripViewSet,self).dispatch(request, *args, **kwargs)
    
    def get_permissions(self):
        """Assign permission based on action."""
        permissions = [IsAuthenticated, IsActivePoolMember]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsPoolOwner)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Add pool to serializer context."""
        context = super(TripViewSet, self).get_serializer_context()
        context['pool'] = self.pool
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateTripSerializer
        return TripModelSerializer

    def get_queryset(self):
        """Return active pool's trips."""
        offset = timezone.now() + timedelta(minutes=10)
        return self.pool.trip_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1
        )