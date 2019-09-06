"""Pools URLs."""

# Django
from django.urls import include, path 

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import pools as pool_views

router = DefaultRouter()
router.register(r'pools', pool_views.PoolViewSet, basename='pool')

urlpatterns = [
    path('',include(router.urls))
]
