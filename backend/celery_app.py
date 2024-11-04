import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('backend')

app.conf.broker_url = 'redis://localhost:6379/0'

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Celery beat schedule to run regularly
app.conf.beat_schedule = {
    'check-prices-and-notify-every-30-minutes': {
        'task': 'core.tasks.check_prices_and_notify_all',
        'schedule': crontab(minute='*/30'),
    },
    'scrape-jerseys-daily': {
        'task': 'core.tasks.scrape_jerseys',
        'schedule': crontab(hour=0, minute=0),
    },
    'update-prices-every-hour': {
        'task': 'core.tasks.update_jersey_prices',
        'schedule': crontab(hour=0, minute=0),
        'args': (),
    },
}
