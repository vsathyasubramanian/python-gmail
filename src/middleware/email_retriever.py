"""
This file contains the EmailRetriever class which hosts the methods containing the business logic to help us with
retrieving emails from server using appropriate connectors.

"""
__author__ = "sathya.v"

import base64
import email

import mysql.connector
from dateutil.parser import parse
from core.google_connector import GoogleConnector

from model.email_dao import EmailDAO
from model.email_entity import EmailEntity
from config.config import DATABASE, DB_PASSWORD, DB_USERNAME


class EmailRetriever:
    """
    Email Retriever class hosting core methods to retrieve email content
        uses the appropriate strategy method
        using connector object authenticates and fetches all the emails from server
        parses the response message and populates the email entity
        stores the email entity in the local database
    """

    def __init__(self):
        self.email_obj_list = []
        self.db_obj = mysql.connector.connect(
            host="localhost",
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DATABASE
        )
        self.email_strategy_mapper = {
            'google': self.email_google_strategy
        }

    def email_google_strategy(self, credentials_path):
        """
        Brief:
            Google Email pull strategy method which pulls emails from google servers and populates the local
            email entity

        Pseudo-code:
            calls authentication module first to authenticate and retrieve the OAuth token
            calls batch get email method to retrieve email content from mail server
            calls parse message method to parse and load the email data onto the entity
        Args:
            credentials_path: Path of the credential and token file

        Returns:

        """
        try:
            google_services_obj = GoogleConnector(credentials_path=credentials_path)
            print("Authenticating...")
            google_services_obj.authenticate()
            print("Authentication Complete...")
            google_services_obj.batch_get_emails(parser=self.parse_and_load_messages, criteria=None)
        except Exception as ex:
            print("exception in connecting to google services and fetching email content :: %s" % ex)
            raise

    def parse_and_load_messages(self, request_id, response, exception):
        """
        Brief:
            Method to parse the response and populate the email entity with the appropriate values
        Args:
            request_id: int request id
            response: response object
            exception: HttpError/None
        Returns:
            mail_entity: object
        """
        try:
            if exception:
                print("HTTP error in processing the request")
                raise
            print("Parsing message request_id ::" + str(request_id), flush=True)
            email_obj = EmailEntity()
            message_str = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))
            email_obj.message_id = response['id']
            email_obj.labels = response['labelIds']
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
        except Exception as ex:
            print("Exception in parsing email content and populating the entity :: %s" % ex)
            raise

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
            self.db_obj.commit()
            return True
        except Exception as ex:
            print("Exception in store_email_snapshot method %s" % ex)
            raise
        finally:
            self.db_obj.close()

    def retrieve_emails(self, credential_path, service=None):
        """
        Brief:
            Fetches the email content an stores in the local database

        Pseudo-code:
            Retrieves and calls the strategy method for the given service
            Calls store data method to store the entity in our DB

        Args:
            credential_path: path of the credential and token file
            service: email service name

        Returns:

        """
        try:
            self.email_strategy_mapper[service](credential_path)
            self.store_email_snapshots()
            return self.email_obj_list
        except Exception as ex:
            print("error in processing email %s " % ex)
