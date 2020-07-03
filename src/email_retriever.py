"""
fetch mails script to fetch emails from gmail after successful OAuth
"""
__author__ = "sathya.v"

import base64
import email

import mysql.connector
from dateutil.parser import parse

from google_connector import GoogleConnector
from config import db_username, db_password, database
from email_dao import EmailDAO
from email_entity import EmailEntity


class EmailRetriever:
    """
    Main class to fetch mails from the server for the authenticated user
    """

    def __init__(self):
        self.email_obj_list = []
        self.db_obj = mysql.connector.connect(
            host="localhost",
            user=db_username,
            password=db_password,
            database=database
        )
        self.fetch_email_strategy_mapper = {
            'google': self.fetch_email_google_strategy
        }

    def fetch_email_google_strategy(self):
        """
        Brief:
            Google Email pull strategy method which pulls emails from google servers and populates the local
            email entity

        Pseudo-code:
            calls authentication module first to authenticate and retrieve the OAuth token
            calls fetch email method to retrieve email content from mail server
            calls parse message method to parse and load the email data onto the entity

        Returns:

        """
        google_services_obj = GoogleConnector(credentials_file='credentials.json')
        print("Authenticating...")
        google_services_obj.authenticate()
        print("Authentication Complete...")
        google_services_obj.batch_get_emails(parser=self.parse_and_load_messages, criteria=None)

    def parse_and_load_messages(self, *args):
        """
        Brief:
            Method to parse the response and populate the entity with the appropriate values
        Args:
            *args
        Returns:
            mail_entity: object
        """
        count = args[0]
        message = args[1]
        print("Parsing message count ::" + str(count), flush=True)
        email_obj = EmailEntity()
        message_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        email_obj.message_id = message['id']
        email_obj.labels = message['labelIds']
        mime_message = email.message_from_string(message_str.decode('ascii'))
        email_obj.from_address = mime_message['From']
        email_obj.to_address = mime_message['To']
        email_obj.subject = mime_message['Subject']
        email_obj.date = parse(mime_message['Date'], ignoretz=True)
        for parts in mime_message.walk():
            if parts.get_content_type() == 'text/plain':
                if parts.get('Content-Transfer-Encoding'):
                    message_content = base64.urlsafe_b64decode(parts.get_payload().encode('UTF-8'))
                    email_obj.content = message_content.decode('UTF-8')
                else:
                    email_obj.content = parts.get_payload()
        self.email_obj_list.append(email_obj)

    def store_email_snapshots(self):
        """
        Brief:
            Method to store the fetched emails in the database.
        Returns:
            Status: True/False
        """
        try:
            dao_obj = EmailDAO(self.db_obj.cursor(dictionary=True))
            dao_obj.bulk_insert_email_snapshot(self.email_obj_list)
            print("Email snapshot stored\n")
            return True
        except Exception as ex:
            print("Exception in store_email_snapshot method %s" % ex)
            raise
        finally:
            self.db_obj.commit()
            self.db_obj.close()

    def fetch_emails(self, service=None):
        """
        Brief:
            fetches the email content an stores in the local database

        Pseudo-code:
            retrieves and calls the strategy method for the given service
            calls store data method to store the entity in our DB

        Args:
            service: email service name

        Returns:

        """
        try:
            self.fetch_email_strategy_mapper[service]()
            self.store_email_snapshots()
            return self.email_obj_list
        except Exception as ex:
            print("error in processing email %s " % ex)