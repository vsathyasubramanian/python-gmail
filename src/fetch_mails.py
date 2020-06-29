"""
fetch mails script to fetch emails from gmail after successful OAuth
"""
__author__ = "sathya.v"

import base64
import email

import mysql.connector
from apiclient import errors
from dateutil.parser import parse
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
from pyfiglet import Figlet

from authenticate import Authenticate
from config import db_username, db_password, database
from console import ConsolePrompt
from email_dao import EmailDAO
from email_entity import EmailEntity


class FetchMails():
    """
    Main class to fetch mails from the server for the authenticated user
    """

    def __init__(self):
        self.service = None
        self.user_id = 'me'
        self.email_obj_list = []
        self.console_obj = ConsolePrompt()
        self.oauth_obj = None
        self.db_obj = mysql.connector.connect(
            host="localhost",
            user=db_username,
            password=db_password,
            database=database
        )

    def _fetch_msg_ids(self, criteria=None):
        """
        Brief:
            helper method to fetch the list of message ids which meets the given criteria
        Args:
            criteria (): additional criteria if any

        Returns:
            list of message_ids
        """
        response = self.service.users().messages().list(userId=self.user_id, q=criteria).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId=self.user_id,
                                                            pageToken=page_token).execute()
            messages.extend(response['messages'])
        message_id_list = []
        for message in messages:
            message_id_list.append(message['id'])
        return message_id_list

    def _parse_messages(self, *args):
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
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        # import pdb;
        # pdb.set_trace()
        email_obj.msg_id = message['id']
        email_obj.labels = message['labelIds']
        mime_msg = email.message_from_string(msg_str.decode('ascii'))
        email_obj.from_address = mime_msg['From']
        email_obj.to_address = mime_msg['To']
        email_obj.subject = mime_msg['Subject']
        # email_obj.date = datetime.datetime.strptime(mime_msg['Date'], '%a, %d %b %Y %H:%M:%S %Z')
        email_obj.date = parse(mime_msg['Date'], ignoretz=True)
        for parts in mime_msg.walk():
            if parts.get_content_type() == 'text/plain':
                if parts.get('Content-Transfer-Encoding'):
                    my_msg = base64.urlsafe_b64decode(parts.get_payload().encode('UTF-8'))
                    email_obj.content = my_msg.decode('UTF-8')
                else:
                    email_obj.content = parts.get_payload()
        self.email_obj_list.append(email_obj)

    def _fetch_email_content(self, message_id_list):
        """
        Brief:
            Method to fetch the email content of the given mail ids
            Using batch call to reduce network call numbers and increase throughput
        Args:
            message_id_list ():
        Returns:
            list of email contents: list of dict

        """
        batch = BatchHttpRequest()
        for msg_id in message_id_list:
            batch.add(self.service.users().messages().get(userId='me', id=msg_id, format='raw'),
                      callback=self._parse_messages)
        batch.execute()

    def fetch_emails(self):
        """
        Brief: Method to fetch the emails from gmail server using the OAuth object for authentication and populate
        the local DB with the email data Returns: status : Boolean

        """
        try:
            self.service = build('gmail', 'v1', credentials=self.oauth_obj.cred)
            message_id_list = self._fetch_msg_ids()
            self._fetch_email_content(message_id_list)
            dao_obj = EmailDAO(self.db_obj.cursor(dictionary=True))
            dao_obj.bulk_insert_email_snapshot(self.email_obj_list)
            print("Email snapshot stored\n")
            self.console_obj.print_email_snapshot(self.email_obj_list)
            return True
        except errors.HttpError as error:
            print("Exception in fetch email method %s" % error)
            raise
        except Exception as ex:
            print("Exception in fetch email method %s" % ex)
            raise
        finally:
            self.db_obj.commit()
            self.db_obj.close()

        # for msg_id in message_id_list:
        #     response = self.service.users().messages().modify(userId='me', id=msg_id,
        #                                                       body={'addLabelIds': ['UNREAD']}).execute()

    def trigger_script(self):
        """
        Brief:
            Driver method to start the email fetch process
            calls authentication module first to authenticate and retrieve the OAuth token
            calls fetch email method to retrieve email content from gmail
            calls parse message method to parse and load the email data onto the entity
            calls store data method to store the entity in our DB
        Returns:
            status : Boolean
        """
        try:
            oauth_obj = Authenticate()
            print("Authenticating...")
            oauth_obj.authenticate()
            print("Authentication Complete...")
            self.oauth_obj = oauth_obj
            self.fetch_emails()
        except Exception as ex:
            print("error in processing email %s " % ex)


if __name__ == "__main__":
    f = Figlet(font='slant')
    print(f.renderText('Email Manager'))
    fetch_email_obj = FetchMails()
    fetch_email_obj.trigger_script()
