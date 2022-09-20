from celery import Celery
from celery.schedules import crontab

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesite.settings')


app = Celery('thesite')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
        "sendit": {
            "task": "stocks.tasks.massStockQuery",
#         "schedule": 20.0
          "schedule": crontab(hour=21, minute=0, day_of_week='mon,tue,wed,thu,fri')
            }
}

app.autodiscover_tasks()
