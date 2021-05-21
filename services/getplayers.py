from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = './services/keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
PLAYER_TABLE = 'Players!A2:K'
STATS_TABLE = 'Results!A2:O'
STATS_TABLE_WRITE = 'Results!A1:AA1000'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SERVICE = build('sheets', 'v4', credentials=creds)

sheet = SERVICE.spreadsheets()
result1 = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=PLAYER_TABLE).execute()

result2 = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                   range=STATS_TABLE).execute()

def _make_players(result1):
    values = result1.get('values', [])
    player_names = ([row[0] for row in values])
    player_names.sort()
    all_players = []
    class Player:
        def __init__(self, name, score, stat):
            self.name = name
            self.score = score
            self.stat = stat
    for row in values:
        all_players.append( Player( row[0], row[6], row[10] ))
    return all_players, player_names

def _make_stats(result2):
    values = result2.get('values', [])
    all_stats = []
    class Stats:
        def __init__(self, date, team_a_result, team_b_result):
            self.date = date
            self.team_a_result = team_a_result
            self.team_b_result = team_b_result
    for row in values:
        all_stats.append( Stats( row[0], row[1], row[2] ))
    return all_stats

def _make_player_stats(result1):
    values = result1.get('values', [])
    player_stats = []
    class PlayerStats:
        def __init__(self, name, wins, draws, losses, total):
            self.name = name
            self.wins = wins
            self.draws = draws
            self.losses = losses
            self.total = total
    for row in values:
        player_stats.append( PlayerStats( row[0], row[7], row[8], row[9], row[10] ))
    return player_stats