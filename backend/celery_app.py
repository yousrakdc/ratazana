import os
from celery import Celery
from celery.schedules import crontab
from django.core.mail import send_mail
import logging

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Define your Celery application
app = Celery('backend')

# Use Redis as the message broker
app.conf.broker_url = 'redis://localhost:6379/0'  # Update if needed

# Load configuration from the config module
app.config_from_object('backend.celeryconfig')

# Auto-discover tasks in the backend module
app.autodiscover_tasks(['backend'])

# Set up the Celery beat schedule to run daily
app.conf.beat_schedule = {
    'scrape-jerseys-daily': {
        'task': 'backend.core.tasks.scrape_jerseys',  # Ensure the correct path
        'schedule': crontab(hour=0, minute=0),  # Run once a day at midnight
    },
}

# Set up logging
logger = logging.getLogger(__name__)
