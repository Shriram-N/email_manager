import time
import base64
import re
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from authenticate.authenticate import Authenticate
from db.db_manager import DbManager
from datetime import datetime
from dateutil import parser


class EmailProcessor:

    def __init__(self):
        self.authenticate = Authenticate()
        self.service = self.authenticate.get_service()
        self.db_manager = DbManager()
        self.batch_emails = []

    def parse_email(self, msg):
        """
        Utility function that extracts and returns the meaningful parts of an email
        """
        email_data = {'email_id': msg['id'],
                      'thread_id': msg['threadId']}
        headers = msg['payload']['headers']

        email_data['from_email'] = next(header['value'] for header in headers if header['name'] == 'From')
        email_data['to_email'] = next(header['value'] for header in headers if header['name'] == 'To')
        email_data['subject'] = next(header['value'] for header in headers if header['name'] == 'Subject')
        received_at = next(header['value'] for header in headers if header['name'] == 'Date')
        email_data['received_at_datetime'] = parsedate_to_datetime(received_at)

        return email_data

    def fetch_emails(self, batch_size):
        """
        Function to fetch emails from the Gmail API, parse them and store them in a database
        """
        results = self.service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])

        if not messages:
            print("No new messages.")
        else:
            print("Message count:", len(messages))

        for idx, message in enumerate(messages):
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = self.parse_email(msg)
            email_data['email_id'] = message['id']
            # email_id, thread_id, received_at, from_email, to_email, subject
            self.batch_emails.append((
                email_data['email_id'],
                email_data['thread_id'],
                email_data['received_at_datetime'],
                email_data['from_email'],
                email_data['to_email'],
                email_data['subject']
            ))

            # If the batch size is reached, insert emails into the database
            if (idx + 1) % batch_size == 0:
                self.db_manager.insert_emails(self.batch_emails)
                self.batch_emails = []

        # Insert any remaining emails into the database
        if self.batch_emails:
            self.db_manager.insert_emails(self.batch_emails)


if __name__ == '__main__':
    email_processor = EmailProcessor()
    email_processor.fetch_emails(batch_size=100)
