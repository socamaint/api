"""
WSGI config for socamaint project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'socamaint.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'socamaint.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socamaint.settings')

application = get_wsgi_application()
