import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these vars, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
RANGE_NAME = 'Players!A2:G'
WRITE_RANGE_NAME = 'Results!A1:AA1000'

creds = None
PICKLE_PATH = os.path.join(
    os.path.dirname(__file__),
    'token.pickle'
)

if os.path.exists(PICKLE_PATH):
    with open(PICKLE_PATH, 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(
                os.path.dirname(__file__),
                'credentials.json'
            ), SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(PICKLE_PATH, 'wb') as token:
#    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token, protocol=2)
SERVICE = build('sheets', 'v4', credentials=creds)

def _fetch_sheet():
    sheet = SERVICE.spreadsheets()
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
def _make_players(sheet_values):
    values = sheet_values.get('values', [])
    player_names = ([row[0] for row in values])
    player_names.sort()
    all_players = []
    class Player:
        def __init__(self, name, score):
            self.name = name
            self.score = score
    for row in values:
        all_players.append( Player( row[0], row[6] ))
    return all_players, player_names