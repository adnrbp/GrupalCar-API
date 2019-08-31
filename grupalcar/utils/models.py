"""Django models utilities."""

#Django
from django.db import models

class GrupalModel(models.Model):
    """ Grupal Car base model.

    GrupalModel acts as an abstract base class from which every
    other model in the project will inherit. 
    The following attributes will be provided:
        + created (DateTime): Store the creation time of the object.
        + modified (DateTime): Store the modification time of the object.
    """

    created = models.DateTimeField(
        'created at', 
        auto_now_add=True,
        help_text='Date time of the object creation'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time of the object modification'
    )

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']