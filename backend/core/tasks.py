import logging
from core.models import Jersey, Alert, Like
from celery import shared_task
from django.core.management import call_command
from pathlib import Path
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import os
from django.db import transaction

# Set up logging
logger = logging.getLogger(__name__)

# Define the base directory for file path management
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path to the OAuth2 token for Gmail API
token_path = os.path.join(BASE_DIR, 'backend/core/token.json')
print(f"Token path: {token_path}")

def send_email_via_gmail_api(to_email, subject, body):
    """Send an email using Gmail API."""
    try:
        # Load OAuth2 credentials from token.json
        credentials = Credentials.from_authorized_user_file(token_path, scopes=[
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.modify'
        ])

        # Refresh credentials if expired
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=credentials)

        # Create the email message
        message = MIMEText(body)
        message['To'] = to_email
        message['From'] = 'ratazana.staff@gmail.com'
        message['Subject'] = subject

        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Prepare the email message for sending
        message_body = {
            'raw': raw_message
        }

        # Send the email
        service.users().messages().send(userId='me', body=message_body).execute()
        print(f"Email sent successfully to {to_email}")
    except HttpError as error:
        logger.error(f'An error occurred: {error}')
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        
@shared_task(name='core.tasks.update_jersey_prices', max_retries=0)
def update_jersey_prices():
    update_report = {
        "total_processed": 0,
        "successfully_updated": 0,
        "errors": [],
        "no_change": 0
    }
    
    try:
        scraped_data = scrape_jerseys()
        
        if not scraped_data:
            logger.warning("No data returned from scrape_jerseys.")
            return "No data to update prices.", update_report

        with transaction.atomic():
            for jersey_data in scraped_data:
                update_report["total_processed"] += 1
                try:
                    jersey = Jersey.objects.get(id=jersey_data['id'])
                    if jersey.price != jersey_data['new_price']:
                        old_price = jersey.price
                        jersey.price = jersey_data['new_price']
                        jersey.save()
                        notify_price_drop(jersey)
                        update_report["successfully_updated"] += 1
                        logger.info(f"Updated jersey {jersey.id} price from {old_price} to {jersey.price}")
                    else:
                        update_report["no_change"] += 1
                except Exception as e:
                    update_report["errors"].append(f"Error updating jersey {jersey_data['id']}: {str(e)}")
                    logger.error(f"Error updating jersey {jersey_data['id']}: {str(e)}")

        return "Price update completed", update_report
    except Exception as e:
        logger.error(f"Error in update_jersey_prices: {str(e)}")
        update_report["errors"].append(f"General error: {str(e)}")
        return f"Error updating prices: {str(e)}", update_report


@shared_task
def send_email_notification(email, jersey_id, new_price):
    """Send an email notification about a jersey price drop."""
    try:
        jersey = Jersey.objects.get(id=jersey_id)
        subject = 'RATAZANA Price Alert: Price Drop on Liked Jersey!'
        message_body = (
            f'Good news! The price for the {jersey.brand} {jersey.team} jersey you liked has dropped! '
            f'The new price is £{new_price}.'
        )
        send_email_via_gmail_api(email, subject, message_body)
        logger.info(f"Email sent to {email} for jersey: {jersey.id}")
    except Jersey.DoesNotExist:
        logger.error(f"Jersey with ID {jersey_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")

@shared_task(name='core.tasks.check_prices_and_notify')
def check_prices_and_notify(jersey_id):  # Ensure it accepts the jersey_id parameter
    try:
        # Fetch the jersey by its ID
        jersey = Jersey.objects.get(id=jersey_id)
    except Jersey.DoesNotExist:
        logger.warning(f"Jersey with id {jersey_id} does not exist.")
        return

    liked_jerseys = Like.objects.filter(jersey=jersey).select_related('user')
    
    if not liked_jerseys.exists():
        logger.warning("No users liked this jersey.")
        return

    logger.info(f"Checking prices for {jersey}: {len(liked_jerseys)} users liked this jersey.")
    
    current_price = jersey.get_current_price()

    logger.info(f"Current price for {jersey}: {current_price}, Last known price: {jersey.last_known_price}")

    if current_price is not None and jersey.last_known_price is not None:
        if current_price < jersey.last_known_price:
            logger.info(f"Price drop detected for {jersey}: from {jersey.last_known_price} to {current_price}")

            for liked_jersey in liked_jerseys:
                notify_price_drop(liked_jersey.user, jersey, current_price)

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

@shared_task(name='backend.core.tasks.scrape_jerseys')
def scrape_jerseys():
    """Task to run the jersey scraping command."""
    logger.info("Starting jersey scraping task.")
    try:
        # Call the management command
        call_command('scrape_jerseys')
        logger.info("Jersey scraping task completed successfully.")
    except Exception as e:
        logger.error(f"Error during jersey scraping task: {str(e)}")
