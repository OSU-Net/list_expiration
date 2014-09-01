"""
WSGI config for list_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os,sys

sys.path.append('/data/ssg-test/htdocs/list_expiration')
sys.path.append('/data/ssg-test/htdocs/list_expiration/list_site')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "list_site.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
