from django.core.management.base import BaseCommand
from core.models import Jersey, Alert, Like
from core.tasks import send_email_notification
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check and trigger alerts for price changes, including liked jerseys.'

    def handle(self, *args, **kwargs):
        self.check_alerts_for_all_users()
        self.check_liked_jerseys()

        self.stdout.write(self.style.SUCCESS('Price alerts and notifications processed successfully.'))

    def check_alerts_for_all_users(self):
        """Check and trigger alerts for price drops across all jerseys."""
        alerts = Alert.objects.filter(status='active')
        for alert in alerts:
            jersey = alert.jersey
            current_price = jersey.price

            # Check for price drop
            if alert.alert_type == 'price_drop' and current_price < jersey.last_known_price:
                alert.trigger_alert()
                logger.info(f"Triggered price drop alert for Jersey ID {jersey.id} and Alert ID {alert.id}.")

    def check_liked_jerseys(self):
        """Check liked jerseys for price drops and notify users."""
        liked_jerseys = Like.objects.select_related('jersey', 'user').all()
        if not liked_jerseys:
            logger.warning("No liked jerseys found.")
            return

        logger.info(f"Checking prices for {len(liked_jerseys)} liked jerseys.")
        
        for liked_jersey in liked_jerseys:
            jersey = liked_jersey.jersey
            current_price = jersey.get_current_price()

            logger.info(f"Current price for {jersey}: {current_price}, Last known price: {jersey.last_known_price}")

            # If price has dropped, notify user
            if current_price is not None and jersey.last_known_price is not None:
                if current_price < jersey.last_known_price:
                    logger.info(f"Price drop detected for {jersey}: from {jersey.last_known_price} to {current_price}")
                    
                    # Notify the user via email
                    notify_price_drop(liked_jersey.user, jersey, current_price)
                    
                    # Update last known price
                    jersey.last_known_price = current_price
                    jersey.save()
                else:
                    logger.info(f"No price drop for {jersey}.")
            else:
                logger.warning(f"Price data is missing for {jersey}.")

def notify_price_drop(user, jersey, current_price):
    """Notify user about the price drop of a liked jersey."""
    logger.info(f"Triggering email for user: {user.email} for jersey: {jersey.id}")
    send_email_notification.delay(user.email, jersey.id, current_price)
