"""Pool serializers."""

# Django Rest Framework
from rest_framework import serializers

# Model
from grupalcar.pools.models import Pool

class PoolModelSerializer(serializers.ModelSerializer):
    """Pool model serializer."""

    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=3000
    )
    is_limited = serializers.BooleanField(default=False)

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
        read_only_fields = (
            'is_public',
            'verified',
            'trips_offered',
            'trips_taken'
        )
    def validate(self,data):
        """Ensure both members_limit and is_limited are present."""
        members_limit = data.get('members_limit',None)
        is_limited = data.get('is_limited', None)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidateError("If pool is limited, a member limit must be provided")
        return data