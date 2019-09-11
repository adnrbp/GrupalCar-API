"""Profile serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from grupalcar.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""
    
    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'picture',
            'biography',
            'trips_taken',
            'trips_offered',
            'reputation'
        )
        read_only_fields = (
            'trips_taken',
            'trips_offered',
            'reputation'
        )