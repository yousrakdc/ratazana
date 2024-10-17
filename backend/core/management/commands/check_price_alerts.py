from django.core.management.base import BaseCommand
from backend.core.tasks import check_prices_and_notify  # Import the Celery task
from core.models import Jersey, Alert

class Command(BaseCommand):
    help = 'Check jersey prices and send notifications for price drops'

    def handle(self, *args, **kwargs):
        check_prices_and_notify.delay()  # Call the task asynchronously
        self.stdout.write(self.style.SUCCESS('Started price checking task.'))

def check_price_alerts(user):
    # Get all jerseys to check their prices
    jerseys = Jersey.objects.all()
    
    for jersey in jerseys:
        # Check if the current price is less than the last known price
        if jersey.price < jersey.last_known_price:
            # Create an alert for the user
            alert = Alert(jersey=jersey, user=user)  # Create an alert without a target price
            alert.save()  # Save the alert to the database
            print(f"Alert created for Jersey ID: {jersey.id} - New Price: {jersey.price}")

        # Update the last known price to the current price
        jersey.last_known_price = jersey.price
        jersey.save()

