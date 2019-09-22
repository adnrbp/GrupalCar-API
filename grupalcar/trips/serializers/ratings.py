"""Ratings serializers."""

# Django
from django.db.models import Avg

# Django REST Framework
from rest_framework import serializers

# Models
from grupalcar.trips.models import Rating


class CreateTripRatingSerializer(serializers.ModelSerializer):
    """Create trip serializer."""

    rating = serializers.IntegerField(min_value=1, max_value=5)
    comments = serializers.CharField(required=False)

    class Meta:
        """Meta class."""

        model = Rating
        fields = ('rating', 'comments')

    def validate(self, data):
        """Verify rating hasn't been emitted before."""
        user = self.context['request'].user
        trip = self.context['trip']

        if not trip.passengers.filter(pk=user.pk).exists():
            raise serializers.ValidationError('User is not a passenger')

        previous_rating = Rating.objects.filter(
            pool=self.context['pool'],
            trip=trip,
            rating_user=user,
        )
        if previous_rating.exists():
            raise serializers.ValidationError('Rating have already been emitted!')
        return data

    def create(self, data):
        """Create rating."""
        offered_by = self.context['trip'].offered_by

        Rating.objects.create(
            pool=self.context['pool'],
            trip=self.context['trip'],
            rating_user=self.context['request'].user,
            rated_user=offered_by,
            **data
        )

        trip_avg = round(
            Rating.objects.filter(
                pool=self.context['pool'],
                trip=self.context['trip']
            ).aggregate(Avg('rating'))['rating__avg'],
            1
        )
        self.context['trip'].rating = trip_avg
        self.context['trip'].save()

        user_avg = round(
            Rating.objects.filter(
                rated_user=offered_by
            ).aggregate(Avg('rating'))['rating__avg'],
            1
        )
        offered_by.profile.reputation = user_avg
        offered_by.profile.save()

        return self.context['trip']