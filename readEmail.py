from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path
from httplib2 import Http
from oauth2client import file, client, tools
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():

    data_folder = Path("readEmailPython/")
    file_to_open = data_folder / "credentials.json"

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(file_to_open, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    messages = messages[0]

    if not messages:
        print("No messages found.")
    else:
        print("Message snippets:")
        msg = service.users().messages().get(userId='me', id=messages['id']).execute()
        str1 = msg['snippet']
        print(str1)
        print(re.findall('\d+', str1))
        a = re.findall('\d+', str1)
        b = a[-2:]
        digit_confirmation_code = b[0] + b[1]
        digit_confirmation_code = int(digit_confirmation_code)
        print(digit_confirmation_code)

if __name__ == '__main__':
    main()
