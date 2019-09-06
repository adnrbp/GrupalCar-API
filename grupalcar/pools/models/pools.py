""" Pool model."""

# Django
from django.db import models

#Utilities
from grupalcar.utils.models import GrupalModel

class Pool(GrupalModel):
    """Pool model.
    A Pool is a private group where trips are offered and taken
    by its members. To join a Pool a user must receive an unique
    invitation code from an existing Pool member.
    """

    name = models.CharField('pool name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('pool description', max_length=50)
    picture = models.ImageField(upload_to='pools/pictures', blank=True, null=True)

    # Stats
    trips_offered = models.PositiveIntegerField(default=0)
    trips_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified pool',
        default=False,
        help_text='Verified pools are also known as official communities.'
    )

    # Constraints
    is_public = models.BooleanField(
        default=True,
        help_text='Public pools are listed in the main page so everyone know about their existence.'
    )

    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='Limited pools can grow up to a fixed number of members.'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If pool is limited, this will be the limit on the number of members.'
    )


    def __str__(self):
        """Return pool name."""
        return self.name

    class Meta(GrupalModel.Meta):
        """Meta class."""

        ordering = ['-trips_taken', '-trips_offered']