
from celery.schedules import crontab

# Broker settings
broker_url = 'redis://localhost:6379/0'

# Result backend settings (optional)
result_backend = 'redis://localhost:6379/0'

# Timezone settings
timezone = 'UTC' 
enable_utc = True

# Task serialization
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# Beat schedule (optional, if using Celery Beat)
beat_schedule = {
    'scrape-jerseys-daily': {
        'task': 'core.tasks.scrape_jerseys',
        'schedule': crontab(hour=0, minute=0),
    },
}