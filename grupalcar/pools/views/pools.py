"""Pool views."""

# Django Rest Framework
from rest_framework import viewsets

# Serializers
from grupalcar.pools.serializers import PoolModelSerializer

# Models
from grupalcar.pools.models import Pool

class PoolViewSet(viewsets.ModelViewSet):
    """Pool view set."""

    queryset = Pool.objects.all()
    serializer_class = PoolModelSerializer