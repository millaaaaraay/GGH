"""
WSGI config for gghweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For moreinformation on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gghweb.settings')
  
application = get_wsgi_application()
 