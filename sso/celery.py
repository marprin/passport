from django.conf import settings
from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sso.settings.base")
app = Celery("sso")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks()
