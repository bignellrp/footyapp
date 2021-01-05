from __future__ import print_function
import pickle, os.path, sys, heapq
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
RANGE_NAME = 'Sheet2!A2:G'
WRITE_RANGE_NAME = 'Sheet3!A1:AA1000'

def googlefunction():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token, protocol=2)
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
    values = result.get('values', [])
    player_names = ([row[0] for row in values])
    all_players = []
    class Player:
        def __init__(self, name, score):
            self.name = name
            self.score = score
    for row in values:
        all_players.append( Player( row[0], row[6] ))
    return player_names, all_players