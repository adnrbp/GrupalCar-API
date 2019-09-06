"""Pools admin."""

# Django
from django.contrib import admin

# Model
from grupalcar.pools.models import Pool


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    """Pool admin."""

    list_display = (
        'slug_name',
        'name',
        'is_public',
        'verified',
        'is_limited',
        'members_limit'
    )
    search_fields = ('slug_name', 'name')
    list_filter = (
        'is_public',
        'verified',
        'is_limited'
    )