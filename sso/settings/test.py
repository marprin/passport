from .base import *

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache",}}

DEBUG = True
CELERY_ALWAYS_EAGER = True
