"""Pools URLs."""

# Django
from django.urls import include, path 

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import pools as pool_views
from .views import memberships as membership_views

router = DefaultRouter()
router.register(r'pools', pool_views.PoolViewSet, basename='pool')
router.register(
    r'pools/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
)

urlpatterns = [
    path('',include(router.urls))
]
