import os
import base64
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

BASE_DIR = Path(__file__).resolve().parent.parent.parent 

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

def send_email_via_gmail_api(to_email, subject, body, from_email='ratazana.staff@gmail.com'):
    try:
        # Load the credentials from the correct path
        token_path = BASE_DIR / 'token.json'
        credentials = Credentials.from_authorized_user_file(token_path, SCOPES)

        # Refresh credentials if expired
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=credentials)

        # Create the email message
        message = MIMEText(body)
        message['to'] = to_email
        message['from'] = from_email
        message['subject'] = subject

        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Prepare the email message for sending
        message = {
            'raw': raw_message
        }

        # Send the email
        service.users().messages().send(userId='me', body=message).execute()
        print(f'Email sent successfully to {to_email}')

    except HttpError as error:
        print(f'An error occurred: {error}')

send_email_via_gmail_api("yousrakdc@gmail.com", "Test Subject", "This is a test email.")
