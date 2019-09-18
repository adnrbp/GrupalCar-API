"""Main URLs module."""

# Django Configurations
from django.conf import settings

from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path("", include(('grupalcar.pools.urls','pools'),namespace='pools')),
    path("", include(('grupalcar.users.urls','users'),namespace='users')),
    path("", include(('grupalcar.trips.urls','trips'),namespace='trips')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
