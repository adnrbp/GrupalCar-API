"""User model."""

#Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#Utilities
from grupalcar.utils.models import GrupalModel

class User(GrupalModel, AbstractUser):
    """User model.

    Extends Django Abstract User, 
    - change username field to email field
    - add some extra fields.
    """
    # Username field
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    # Phone Field
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )

    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Filter fields
    is_client = models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'Help distinguish users and perform queries.'
            'Clients are the main type of user'
        )
    )

    is_verfied = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )


    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
