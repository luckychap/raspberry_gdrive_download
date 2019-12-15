#!/usr/bin/python
from __future__ import print_function
import pickle
import os.path, io
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

import auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS = 'credentials.json'
TOKEN = 'token.pickle'
KUBKO = '1CN-OHaUPimULMtbxJkSjW0V3n_llj2qD'
PICTURE_DEST = '/home/lucky/Downloads/drive/'
NUMBER_OF_PICTURES = 1000

authApp = auth.auth(SCOPES,CREDENTIALS,TOKEN)
creds = authApp.get_credentials()

drive_service = build('drive', 'v3', credentials=creds)

def searchFile(query,fields='id, name, mimeType, parents',size=100):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(%s)" % fields,q=query).execute()
    items = results.get('files', [])
    return items

def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())


# if __name__ == '__main__':
#     main()
pictures = searchFile("'%s' in parents and mimeType = 'image/jpeg'" % KUBKO,"id, name",NUMBER_OF_PICTURES)
print(pictures)
for picture in pictures:
    print(picture['name'])
    downloadFile(picture['id'],PICTURE_DEST + picture['name'])
