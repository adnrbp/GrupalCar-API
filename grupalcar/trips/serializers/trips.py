"""Trips serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from grupalcar.trips.models import Trip
from grupalcar.pools.models import Membership

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

