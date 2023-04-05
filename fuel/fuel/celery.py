import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTING_MODULE", "fuel.settings")
app = Celery("fuel")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every' : {
        'task' : 'statistic.tasks.gps_imitation',
        'schedule' : crontab(),
    },
    'every' : {
            'task' : 'statistic.tasks.check_imitation',
            'schedule' : crontab(),
        },
}

