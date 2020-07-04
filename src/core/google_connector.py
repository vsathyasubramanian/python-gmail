"""
Google API interface class
"""
__author__ = "sathya.v"

import os.path
import pickle

from apiclient import errors
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest

from config.config import SCOPES


class GoogleConnector:
    """
    Google connector class hosting methods to interact with Google Servers for
     Authentication - OAuth
     Email retrieval
     Email Updation
    """

    def __init__(self, credentials_path):
        self.scope = SCOPES
        self.token_file = credentials_path + 'token.pickle'
        self.user_id = 'me'
        self.credentials_file = credentials_path + 'credentials.json'
        self.cred = None
        self.service = None

    def __fetch_message_ids(self, criteria=None):
        """
        Brief:
            Method to fetch the list of message ids which meets the given criteria
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

    def authenticate(self):
        """
        :Brief:
            Method to trigger OAuth and get the token and store it in the token.pickle file for future use

            The file token.pickle stores the user's access and refresh tokens, and is created automatically when the
            authorization flow completes for the first time.

        Returns:
        """
        try:
            self.cred = None
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    self.cred = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not self.cred or not self.cred.valid:
                if self.cred and self.cred.expired and self.cred.refresh_token:
                    self.cred.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.scope)
                    self.cred = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(self.token_file, 'wb') as token:
                    pickle.dump(self.cred, token)
            # to check if we can have this else where
            self.service = build('gmail', 'v1', credentials=self.cred)
            return True
        except errors.HttpError as error:
            print("Exception in authenticating %s" % error)
            return False
        except Exception as ex:
            print("Exception in authenticating %s" % ex)
            return False

    def batch_get_emails(self, parser=None, criteria=None):
        """
        Brief:
            Method to fetch the message content of the emails which meets the given criteria
        Args:
            criteria : additional criteria if any
            parser : method used to parse the raw message response from Gmail API and populate the local entity

        Returns:
            email contents
        """
        try:
            message_id_list = self.__fetch_message_ids(criteria)
            batch = BatchHttpRequest()
            for message_id in message_id_list:
                batch.add(self.service.users().messages().get(userId=self.user_id, id=message_id, format='raw'),
                          callback=parser)
            batch.execute()
        except errors.HttpError as error:
            print("Exception in fetch email method %s" % error)
            raise
        except Exception as ex:
            print("Exception in fetch email method %s" % ex)
            raise

    def batch_modify_emails(self, body_dict):
        """
        Brief:
            Method to fetch the message content of the emails which meets the given criteria
        Args:
            body_dict : labels and message ids to be modified in google

        Returns:
            status
        """
        try:
            modify_response = self.service.users().messages().batchModify(userId=self.user_id,
                                                                          body=body_dict).execute()
            return modify_response
        except errors.HttpError as error:
            print("Exception in fetch email method %s" % error)
            raise
        except Exception as ex:
            print("Exception in fetch email method %s" % ex)
            raise
