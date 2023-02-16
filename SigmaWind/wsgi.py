"""
WSGI config for SigmaWind project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SigmaWind.settings')
# os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', 'SigmaWind/imagediff/sigmawind001-e00ef8657f10.json')
os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', 'SigmaWind/imagediff/sigmawindapp001-c8de1ff3f146.json')

application = get_wsgi_application()
