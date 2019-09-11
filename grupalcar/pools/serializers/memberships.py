"""Membership serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from grupalcar.users.serializers import UserModelSerializer

# Models
from grupalcar.pools.models import Membership

class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created',read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by',
            'trips_taken', 'trips_offered',
            'joined_at'
        )
        read_only_fields= (
            'user',
            'used_invitations', 'invited_by',
            'trips_taken', 'trips_offered'
        )
