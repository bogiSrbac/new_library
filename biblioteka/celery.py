import os

from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteka.settings')

app = Celery('biblioteka')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Belgrade')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'warning-for-book':{
        'task': 'uljesaKojadinovic.tasks.return_book_duration',
        'schedule': crontab(hour=15, minute=55)
    },
    'membership_expire_duration': {
        'task': 'uljesaKojadinovic.tasks.membership_days_left',
        'schedule': crontab(hour=15, minute=54)
    }
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')