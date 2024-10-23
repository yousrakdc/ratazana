from django.core.management.base import BaseCommand
from core.models import Jersey
from core.tasks import send_email_notification

class Command(BaseCommand):
    help = 'Test sending email notification'

    def handle(self, *args, **kwargs):
        jersey = Jersey.objects.first()
        if jersey:
            email = "8879@holbertonstudents.com"
            new_price = 40.00 
            send_email_notification.delay(email, jersey.id, new_price)
            self.stdout.write(self.style.SUCCESS('Email notification task has been queued.'))
        else:
            self.stdout.write(self.style.ERROR('No jerseys found.'))
