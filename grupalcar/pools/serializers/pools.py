"""Pool serializers."""

# Django Rest Framework
from rest_framework import serializers

# Model
from grupalcar.pools.models import Pool

class PoolModelSerializer(serializers.ModelSerializer):
    """Pool model serializer."""

    class Meta:
        """Meta class."""

        model = Pool
        fields = (
            'id', 'name', 'slug_name',
            'about', 'picture',
            'trips_offered', 'trips_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'
        )