"""Membership model."""

# DJango
from django.db import models 

# Utilities
from grupalcar.utils.models import GrupalModel

class Membership(GrupalModel):
    """Membership model.

    A membership is the table that holds the relationship between
    a user and a Pool.
    """

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    pool = models.ForeignKey("pools.Pool", on_delete=models.CASCADE)

    is_admin=models.BooleanField(
        'pool admin',
        default=False,
        help_text="Pool admins can update the pool's data and manage its members."
    )

    #invitations
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='shared_memberships'
    )

    # Stats
    trips_taken = models.PositiveIntegerField(default=0)
    trips_offered = models.PositiveIntegerField(default=0)

    # Status
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Only active users are allowed to interact in the pool.'
    )

    def __str__(self):
        """Return username and pool."""
        return '@{} at #{}'.format(
            self.user.username,
            self.pool.slug_name
        )