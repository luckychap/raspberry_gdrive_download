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

def qs():
    service = build('drive', 'v3', credentials=creds)
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def searchFile(size,query):
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, mimeType, parents)",q=query).execute()
    items = results.get('files', [])
    return items
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(item)
            # print('{0} ({1})'.format(item['name'], item['id']))

# if __name__ == '__main__':
#     main()
par = searchFile(1,"name = 'Kubko' and mimeType = 'application/vnd.google-apps.folder'")
par_id = par[0]['id']
pic = getattr(searchFile(5,"'%s' in parents and mimeType = 'image/jpeg'" % par_id), 'id')
print(pic)