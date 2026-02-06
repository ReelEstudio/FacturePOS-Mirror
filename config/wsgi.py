""" WSGI config for web project. """ 

import os import django from django.core.wsgi import get_wsgi_application from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try: if not settings.configured: django.setup() settings.SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer' except Exception: pass

application = get_wsgi_application()