"""
WSGI config for Home Books project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# This allows easy placement of apps within the interior
# grupalcar directory.
app_path = os.path.abspath(
	os.path.join(
		os.path.dirname(os.path.abspath(__file__)), 
		os.pardir))

sys.path.append(os.path.join(app_path, 'grupalcar'))



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
