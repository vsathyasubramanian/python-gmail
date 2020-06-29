"""
contains all the methods needed to complete OAuth
"""
__author__ = "sathya.v"

import os.path
import pickle

from apiclient import errors
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from config import SCOPES


class Authenticate():
    """
    main authenticate class with all the OAuth functionalities to connect with gmail servers
    """

    def __init__(self):
        self.scope = SCOPES
        self.token_file = 'token.pickle'
        self.credentials_file = 'credentials.json'
        self.cred = None

    def authenticate(self):
        """
        :Brief:
            Method to trigger OAuth and get the token and store it in the token.pickle file for future use

            The file token.pickle stores the user's access and refresh tokens, and is created automatically when the
            authorization flow completes for the first time.

        :param None: None
        :type None: None
        :return: OAuth credential token
        :rtype: Boolean
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
            return True
        except errors.HttpError as error:
            print("Exception in authenticating %s" % error)
            return False
        except Exception as ex:
            print("Exception in authenticating %s" % ex)
            return False
