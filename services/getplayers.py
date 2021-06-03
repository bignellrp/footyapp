from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

SERVICE_ACCOUNT_FILE = './services/keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
PLAYER_TABLE = 'Players!A2:K'
STATS_TABLE = 'Results!A2:O'
RESULTS_TABLE = 'Results!A1:O'
PLAYERS_TABLE = 'Players!A1:K'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SERVICE = build('sheets', 'v4', credentials=creds)
sheet = SERVICE.spreadsheets()

def _fetch_players_table():
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=PLAYERS_TABLE).execute()
def _fetch_results_table():
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RESULTS_TABLE).execute()

def _get_players_table(players_table):
    ##Get values from player_table
    values = players_table.get('values', [])
    ##Add values to data frame
    df = pd.DataFrame(values[1:], columns=values[0])
    df = df.sort_values(by=['Name'],ascending=True)

    ##Debug: Use the lines below to print a copy of the dataset for testing
    ##Player Table Date in player_data.py
    #print('player_raw_data =', df.to_dict(orient='list'))
    #print('player_df = pd.DataFrame(player_raw_data, columns = ' + str(list(df)) + ')')

    ##Filter Names and convert to list
    player_names = df['Name'].tolist()

    ##Filter All Players
    all_players = df.filter(['Name','Total'])
    all_players['Total'] = pd.to_numeric(all_players['Total'])
    all_players = all_players.to_records(index=False)
    all_players = list(all_players)

    ##Filter Player Stats
    player_stats = df.filter(['Name','Wins','Draws','Losses','Score'])
    player_stats[['Wins','Draws','Losses','Score']] = player_stats[['Wins','Draws','Losses','Score']].apply(pd.to_numeric)
    ##Sort by Score
    player_stats = player_stats.sort_values(by=['Score'],ascending=False)
    player_stats = player_stats.to_records(index=False)
    player_stats = list(player_stats)

    ##Filter Game Stats for Leaderboard
    leaderboard = df.filter(['Name','Score'])
    ##Convert Score to Int
    leaderboard['Score'] = pd.to_numeric(leaderboard['Score'])
    leaderboard = leaderboard.sort_values(by=['Score'],ascending=False)
    leaderboard = leaderboard.head(10)
    leaderboard = leaderboard.to_records(index=False)
    leaderboard = list(leaderboard)
    return all_players, player_names, leaderboard, player_stats

def _get_results_table(results_table):
    ##Get values from results_table
    values = results_table.get('values', [])
    ##Add values to data frame
    df = pd.DataFrame(values[1:], columns=values[0])

    ##Debug: Use the lines below to print a copy of the dataset for testing
    ##Results Table Date in results_data.py
    #print('results_raw_data =', df.to_dict(orient='list'))
    #print('results_df = pd.DataFrame(results_raw_data, columns = ' + str(list(df)) + ')')

    ##Convert date column to datetime
    df['Date'] = pd.to_datetime(df.Date, format='%Y%m%d', errors='ignore')

    ##Filter All Players
    game_stats = df.filter(['Date','Team A Result?','Team B Result?'])
    game_stats = game_stats.tail(10)
    game_stats = game_stats.sort_values(by=['Date'],ascending=False)
    game_stats = game_stats.to_records(index=False)
    game_stats = list(game_stats)

    ##Use data frame shape to work out end row
    end_row = df.shape[0] + 1
    
    #Use iloc to get last row and columns for teama,teamb,dash and date
    teama = df.iloc[-1,5:10]
    teama = list(teama)
    teamb = df.iloc[-1,10:15]
    teamb = list(teamb)
    dash = df.iloc[-1,1]
    date = df.iloc[-1,0]
    return end_row,teama,teamb,dash,date,game_stats