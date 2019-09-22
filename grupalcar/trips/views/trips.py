"""Trip views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from grupalcar.pools.permissions.memberships import IsActivePoolMember
from grupalcar.trips.permissions.trips import IsTripOwner, IsNotTripOwner

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Serializers
from grupalcar.trips.serializers import (
    CreateTripSerializer,
    TripModelSerializer,
    JoinTripSerializer,
    EndTripSerializer,
    CreateTripRatingSerializer,
)

# Models
from grupalcar.pools.models import Pool

# Utilities
from datetime import timedelta
from django.utils import timezone

class TripViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
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
        if self.action in ['update', 'partial_update','finish']:
            permissions.append(IsTripOwner)
        if self.action in ['join','rate']:
            permissions.append(IsNotTripOwner)
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
        if self.action == 'join':
            return JoinTripSerializer
        if self.action == 'finish':
            return EndTripSerializer
        if self.action == 'rate':
            return CreateTripRatingSerializer
        return TripModelSerializer

    def get_queryset(self):
        """Return active pool's trips."""
        if self.action not in ['finish','retrieve', 'rate']:
            offset = timezone.now() + timedelta(minutes=10)
            return self.pool.trip_set.filter(
                departure_date__gte=offset,
                is_active=True,
                available_seats__gte=1
            )
        return self.pool.trip_set.all()

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        """Add requesting user to trip."""
        trip = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            trip,
            data={'passenger': request.user.pk},
            context={'trip': trip,'pool':self.pool},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()
        data = TripModelSerializer(trip).data
        return Response(data,status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        """Called by owners to finish a trip."""
        trip = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            trip,
            data={'is_active': False, 'current_time': timezone.now()},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()
        data = TripModelSerializer(trip).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        """Rate trip."""

        trip = self.get_object()
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['trip'] = trip

        serializer = serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()

        data= TripModelSerializer(trip).data
        return Response(data, status=status.HTTP_201_CREATED)
