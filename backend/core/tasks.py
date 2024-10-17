import logging
from django.core.mail import send_mail
from celery import shared_task
from .models import Jersey
from .management.commands.scrape_jerseys import Command
from django.core.management import call_command

logger = logging.getLogger(__name__)

@shared_task
def check_prices_and_notify():
    """Task to check jersey prices and notify users if the price has dropped."""
    jerseys = Jersey.objects.all() 
    for jersey in jerseys:
        current_price = jersey.get_current_price() 
        notify_if_price_dropped(jersey.id, current_price) 


def notify_if_price_dropped(jersey_id, current_price):
    """Checks if the jersey price has dropped and sends an email notification."""
    try:
        jersey = Jersey.objects.get(id=jersey_id)
        if current_price < jersey.last_known_price:
            send_email_to_user(jersey.user.email, current_price)
            jersey.last_known_price = current_price
            jersey.save() 
            logger.info(f"Price alert sent for jersey ID {jersey_id} to {jersey.user.email}.")
        else:
            logger.info(f"No price drop for jersey ID {jersey_id}. Current price: {current_price}.")
    except Exception as e:
        logger.error(f"Error checking price for jersey ID {jersey_id}: {str(e)}")


def send_email_to_user(email, new_price):
    """Sends an email notification to the user about the price drop."""
    subject = "Price Alert!"
    message = f"The price of the jersey has dropped to £{new_price}."
    try:
        send_mail(subject, message, 'ratazana.staff@gmail.com', [email])
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}")


logger = logging.getLogger(__name__)

@shared_task
def scrape_jerseys():
    """Task to run the jersey scraping command daily."""
    command = Command()  # Instantiate the scrape command
    command.handle()  # Call the handle method to start scraping


@shared_task
def scrape_jerseys():
    logger.info("Starting jersey scraping task.")
    try:
        # Call the management command to scrape jerseys
        call_command('scrape_jerseys')
        logger.info("Jersey scraping task completed successfully.")
    except Exception as e:
        logger.error(f"Error during jersey scraping task: {e}")