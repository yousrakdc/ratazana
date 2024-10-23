import os
import pickle
from django.core.management.base import BaseCommand
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]


class Command(BaseCommand):
    help = 'Generates a new OAuth2 token for Gmail API.'

    def handle(self, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        creds = None
        # Load existing credentials if they exist
        if os.path.exists(os.path.join(BASE_DIR, 'token.pickle')):
            with open(os.path.join(BASE_DIR, 'token.pickle'), 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(BASE_DIR, 'management', 'commands', 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials
            with open(os.path.join(BASE_DIR, 'management', 'commands', 'token.json'), 'w') as token_file:
                token_file.write(creds.to_json())

        self.stdout.write(self.style.SUCCESS('Token generated successfully.'))
