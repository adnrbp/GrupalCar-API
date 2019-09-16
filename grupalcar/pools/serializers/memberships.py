"""Membership serializers."""

# Django
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers

# Serializers
from grupalcar.users.serializers import UserModelSerializer

# Models
from grupalcar.pools.models import Membership, Invitation

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

class AddMemberSerializer(serializers.Serializer):
    """Add member serializer.

    Handle the addition of a new member to a pool.
    Pool object must be provided in the context.
    """

    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self,data):
        """Verify user isn't already a member."""
        pool = self.context['pool']
        user = data

        query_membership = Membership.objects.filter(pool=pool, user=user)
        if query_membership.exists():
            raise serializers.ValidationError('User is already member of this pool')
        return data

    def validate_invitation_code(self,data):
        """Verify code exists and that it is related to the pool."""
        try:
            invitation = Invitation.objects.get(
                code=data,
                pool=self.context['pool'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')

        # To be reused at creation time
        self.context['invitation'] = invitation
        return data
    
    def validate(self,data):
        """Verify that the pool is capable of accepting a new member."""
        pool = self.context['pool']
        if pool.is_limited and pool.members.count() >= pool.members_limit:
            raise serializers.ValidationError('Pool has reached its member limit!') 
        return data
    
    def create(self,data):
        """Create new pool member."""
        pool = self.context['pool']
        invitation = self.context['invitation']
        user = data['user']

        now = timezone.now()

        # Member creation
        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            pool=pool,
            invited_by=invitation.issued_by
        )

        #Update Invitation
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        #Update issuer data (stats)
        issuer = Membership.objects.get(user=invitation.issued_by, pool=pool)
        issuer.used_invitations += 1
        issuer.remaining_invitations -= 1
        issuer.save()

        return member
