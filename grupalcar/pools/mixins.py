"""Django mixins utilities. """

# Django REST Framework
from rest_framework.viewsets import GenericViewSet

# Models
from grupalcar.pools.models import Pool

# Django REST Framework
from rest_framework.generics import get_object_or_404


class AddPoolMixin(GenericViewSet):
    """Add pool mixin
    Manages adding a pool object to views
    that require it.
    """

    def dispatch(self, request, *args, **kwargs):
        """Return the normal dispatch but adds the pool model."""

        slug_name = self.kwargs['slug_name']

        self.pool = get_object_or_404(
            Pool,
            slug_name=slug_name
        )

        return super(AddPoolMixin, self).dispatch(request, *args, **kwargs)