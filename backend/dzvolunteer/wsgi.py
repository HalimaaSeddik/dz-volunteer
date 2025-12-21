"""
WSGI config for dzvolunteer project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dzvolunteer.settings')

application = get_wsgi_application()
