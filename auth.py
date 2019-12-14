from __future__ import print_function
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class auth:
    def __init__(self,SCOPES,CREDENTIALS,TOKEN):
        self.SCOPES = SCOPES
        self.CREDENTIALS = CREDENTIALS
        self.TOKEN = TOKEN
    def get_credentials(self):
        creds = None
        if os.path.exists(self.TOKEN):
            with open(self.TOKEN, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.TOKEN, 'wb') as token:
                pickle.dump(creds, token)
        return creds