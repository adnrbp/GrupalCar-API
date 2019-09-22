"""Trips rating model."""

# Django
from django.db import models

# Utilities
from grupalcar.utils.models import GrupalModel


class Rating(GrupalModel):
    """Trip rating.
    Rates are entities that store the rating a user
    gave to a trip, it ranges from 1 to 5 and it affects
    the trip offerer's overall reputation.
    """

    trip = models.ForeignKey(
        'trips.Trip',
        on_delete=models.CASCADE,
        related_name='rated_trip'
    )
    pool = models.ForeignKey('pools.Pool', on_delete=models.CASCADE)

    rating_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that emits the rating',
        related_name='rating_user',
    )
    rated_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that receives the rating.',
        related_name='rated_user'
    )

    comments = models.TextField(blank=True)

    rating = models.IntegerField(default=1)

    def __str__(self):
        """Return summary."""
        return '@{} rated {} @{}'.format(
            self.rating_user.username,
            self.rating,
            self.rated_user.username,
        )