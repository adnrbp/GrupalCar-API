"""Trips URLs."""

# Django
from django.urls import include, path 

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import trips as trip_views

router = DefaultRouter()
router.register(
    r'pools/(?P<slug_name>[a-zA-Z0-9_-]+)/trips',
    trip_views.TripViewSet,
    basename='trip'
)

urlpatterns = [
    path('',include(router.urls))
]
