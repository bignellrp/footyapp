from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = './services/keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
PLAYER_TABLE = 'Players!A2:K'
STATS_TABLE = 'Results!A2:O'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SERVICE = build('sheets', 'v4', credentials=creds)
sheet = SERVICE.spreadsheets()

def _fetch_player_sheet():
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=PLAYER_TABLE).execute()
def _fetch_stats_sheet():
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=STATS_TABLE).execute()

def _make_players(player_table):
    values = player_table.get('values', [])
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

def _make_stats(stats_table):
    values = stats_table.get('values', [])
    all_stats = []
    class Stats:
        def __init__(self, date, team_a_result, team_b_result):
            self.date = date
            self.team_a_result = team_a_result
            self.team_b_result = team_b_result
    for row in values:
        all_stats.append( Stats( row[0], row[1], row[2] ))
    return all_stats

def _make_player_stats(player_table):
    values = player_table.get('values', [])
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

def _make_score(stats_table):
    values = stats_table.get('values', [])
    score_stats = []
    class ScoreStats:
        def __init__(self, date, scorea, scoreb, teama_1, teama_2, teama_3, teama_4, teama_5, teamb_1, teamb_2, teamb_3, teamb_4, teamb_5):
            self.date = date
            self.scorea = scorea
            self.scoreb = scoreb
            self.teama_1 = teama_1
            self.teama_2 = teama_2
            self.teama_3 = teama_3
            self.teama_4 = teama_4
            self.teama_5 = teama_5
            self.teamb_1 = teamb_1
            self.teamb_2 = teamb_2
            self.teamb_3 = teamb_3
            self.teamb_4 = teamb_4
            self.teamb_5 = teamb_5
    for row in values:
        score_stats.append( ScoreStats( row[0], row[1], row[2], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14] ))
    end_row = len(values) + 1
    return score_stats,end_row