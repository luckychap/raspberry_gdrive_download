#!/usr/bin/python
from __future__ import print_function
import pickle
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS = 'credentials.json'
TOKEN = 'token.pickle'
authApp = auth.auth(SCOPES,CREDENTIALS,TOKEN)
creds = authApp.get_credentials()

drive_service = build('drive', 'v3', credentials=creds)

def searchFile(query,fields='id, name, mimeType, parents',size=100):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(%s)" % fields,q=query).execute()
    items = results.get('files', [])
    return items

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


# if __name__ == '__main__':
#     main()
par = searchFile(1,"name = 'Kubko' and mimeType = 'application/vnd.google-apps.folder'")
par_id = par[0]['id']
pic = getattr(searchFile(5,"'%s' in parents and mimeType = 'image/jpeg'" % par_id), 'id')
print(pic)