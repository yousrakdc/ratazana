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
from decimal import Decimal


logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
        
@shared_task
def check_prices_and_notify():
    liked_jerseys = Like.objects.select_related('jersey', 'user').all()
    logger.info(f"Checking prices for {len(liked_jerseys)} liked jerseys.")
    
    for liked_jersey in liked_jerseys:
        jersey = liked_jersey.jersey
        current_price = jersey.get_current_price()
        logger.info(f"Current price for {jersey}: {current_price}, Last known price: {jersey.last_known_price}")
        
        if current_price < jersey.last_known_price:
            logger.info(f"Price drop detected for {jersey}: from {jersey.last_known_price} to {current_price}")
            notify_price_drop(liked_jersey.user, jersey, current_price)
            jersey.last_known_price = current_price
            jersey.save()
        else:
            logger.info(f"No price drop for {jersey}.")

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
