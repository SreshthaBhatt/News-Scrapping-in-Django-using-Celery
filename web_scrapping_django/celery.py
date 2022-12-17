from __future__ import absolute_import,unicode_literals

import os

from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','web_scrapping_django.settings')

app=Celery('web_scrapping_django')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')

app.conf.beat_schedule={

}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')