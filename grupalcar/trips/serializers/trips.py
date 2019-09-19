"""Trips serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from grupalcar.trips.models import Trip
from grupalcar.pools.models import Membership
from grupalcar.users.models import User

# Serializers
from grupalcar.users.serializers import UserModelSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone

class TripModelSerializer(serializers.ModelSerializer):
    """Trip model serializer."""

    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()

    passengers = UserModelSerializer(read_only=True,many=True)

    class Meta:
        """Meta class."""

        model = Trip
        fields = '__all__'
        read_only_fields = (
            'offered_in', 
            'offered_by', 
            'rating'
        )
    def update(self, instance, data):
        """Allow updates only before departure date."""
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('Ongoing trips cannot be modified.')
        return super(TripModelSerializer, self).update(instance, data)

class CreateTripSerializer(serializers.ModelSerializer):
    """Create trip serializer."""

    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        """Meta class."""

        model = Trip
        exclude = ('offered_in', 'passengers', 'rating', 'is_active')

    def validate_departure_date(self, data):
        """Verify date is not in the past."""
        min_date = timezone.now() + timedelta(minutes=10)
        if data < min_date:
            raise serializers.ValidationError(
                'Departure time must pass at least the next 20 minutes window.'
            )
        return data

    def validate(self,data,):
        """Validate.

        Verify that the person who offers the trip is member
        and also the same user making the request.
        """
        # Validate same user will offer the trip.
        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('Trips offered on behalf of others are not allowed.')

        user = data['offered_by']
        pool = self.context['pool']
        # Validate active member existance
        try:
            membership = Membership.objects.get(
                user=user,
                pool=pool,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the pool.')
        
        # Validate date
        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure date must happen after arrival date.')

        self.context['membership'] = membership
        return data

    def create(self, data):
        """Create trip and update stats"""
        pool = self.context["pool"]
        trip = Trip.objects.create(**data,offered_in=pool)

        # Pool stats
        pool.trips_offered += 1
        pool.save()

        # Membership stats
        membership = self.context['membership']
        membership.trips_offered += 1
        membership.save()

        # Profile stats
        profile = data['offered_by'].profile
        profile.trips_offered += 1
        profile.save()

        return trip

class JoinTripSerializer(serializers.ModelSerializer):
    """Join trip serializer."""

    passenger = serializers.IntegerField()

    class Meta:
        """Meta class."""

        model = Trip
        fields = ('passenger',)

    def validate_passenger(self,data):
        """Verify passenger exists and is a pool member."""
        try:
            user = User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid passenger.')
        
        pool = self.context['pool']
        try:
            membership = Membership.objects.get(
                user=user,
                pool=pool,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the poo.')

        self.context['user'] = user
        self.context['member'] = membership
        return data
    def validate(self,data):
        """Verify trips allow new passengers."""
        trip = self.context['trip']
        if trip.departure_date <= timezone.now():
            raise serializers.ValidationError("You can't join this trip now")
        if trip.available_seats < 1:
            raise serializers.ValidationError("Trip is already full!")
        
        if Trip.objects.filter(passengers__pk=data['passenger']):
            raise serializers.ValidationError('Passenger is already in this trip')
        
        return data
    
    def update(self, instance, data):
        """Add passenger to trip, and update stats."""
        trip = self.context['trip']
        user = self.context['user']

        # Join to trip
        trip.passengers.add(user)
        trip.available_seats -= 1
        #trip.save()

        # Profile stats
        profile = user.profile
        profile.trips_taken += 1
        profile.save()

        # Membership stats
        member = self.context['member']
        member.trips_taken += 1
        member.save()

        # Pool stats
        pool = self.context['pool']
        pool.trips_taken += 1
        pool.save()

        return trip

