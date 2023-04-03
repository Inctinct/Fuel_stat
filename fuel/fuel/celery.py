import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTING_MODULE", "fuel.settings")
app = Celery("fuel")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()