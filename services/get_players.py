from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

SERVICE_ACCOUNT_FILE = './services/keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
RESULTS_TABLE = 'Results!A1:O'
PLAYERS_TABLE = 'Players!A1:G'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SERVICE = build('sheets', 'v4', credentials=creds)
sheet = SERVICE.spreadsheets()

def _fetch_players_table():
    '''Returns sheet values from players table'''
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=PLAYERS_TABLE).execute()
def _fetch_results_table():
    '''Returns sheet values from results table'''
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RESULTS_TABLE).execute()

def _get_players_table(players_table):
    '''Takes in sheet values from players table and returns;
        all_players: a list of all players and their total
        player_names: a list of player names in alpha order
        leaderboard: a list of top10 players and scores
        player_stats: a list of all player stats, win, draw loss'''

    ##Get values from player_table
    values = players_table.get('values', [])

    ##Add values to data frame
    df = pd.DataFrame(values[1:], columns=values[0])
    ##Sort data frame by Name
    df = df.sort_values(by=['Name'],ascending=True)

    ##Debug: Use the lines below to print a copy of the dataset for testing
    ##Player Table Date in player_data.py
    #print('player_raw_data =', df.to_dict(orient='list'))
    #print('player_df = pd.DataFrame(player_raw_data, columns = ' + str(list(df)) + ')')

    ##Filter Names and convert to list
    ##Filter Names and Playing Value and convert to list
    ##player_names = df['Name'].tolist()
    player_names = df.filter(['Name','Playing'])
    ##Convert from df to list without index to be used in forms
    player_names = player_names.to_records(index=False)
    player_names = list(player_names)

    ##Filter All Players
    all_players = df.filter(['Name','Total'])
    ##Convert Total column to numeric so they can be added up
    all_players['Total'] = pd.to_numeric(all_players['Total'])
    ##Convert from df to list without index to be used in forms
    all_players = all_players.to_records(index=False)
    all_players = list(all_players)

    ##Filter Player Stats
    player_stats = df.filter(['Name','Wins','Draws','Losses','Score'])
    ##Convert multiple columns to numeric
    player_stats[['Wins','Draws','Losses','Score']] = player_stats[['Wins','Draws','Losses','Score']].apply(pd.to_numeric)
    ##Sort by Score
    player_stats = player_stats.sort_values(by=['Score'],ascending=False)
    ##Convert from df to list without index to be used in forms
    player_stats = player_stats.to_records(index=False)
    player_stats = list(player_stats)

    ##Filter Game Stats for Leaderboard
    leaderboard = df.filter(['Name','Score'])
    ##Convert Score column to numeric so they can be added up
    leaderboard['Score'] = pd.to_numeric(leaderboard['Score'])
    leaderboard = leaderboard.sort_values(by=['Score'],ascending=False)
    ##Head the top10
    leaderboard = leaderboard.head(10)
    ##Convert from df to list without index to be used in forms
    leaderboard = leaderboard.to_records(index=False)
    leaderboard = list(leaderboard)

    ##Count the number of players in tally
    game_tally = []
    game_player_tally = []
    for row in player_names:
        '''Takes in row of player_names
        and outputs a just the tally column'''
        game_player_tally.append((row[0]))
        game_tally.append((row[1]))
    player_count = 10 - game_tally.count("x")

    return all_players, player_names, leaderboard, player_stats, player_count, game_player_tally

def _get_results_table(results_table):
    '''Takes in sheet values from results table and returns;
        end_row: The end row from the table to be used when updating spreadsheet
        teama: A list of players from last row from teama
        teamb: A list of players from last row from teamb
        dash: The value from column B that either contains a dash or a score
        date: The date from the last row that should be last wednesdays date
        game_stats: A list'''

    ##Get values from results_table
    values = results_table.get('values', [])
    ##Add values to data frame
    df = pd.DataFrame(values[1:], columns=values[0])

    ##Debug: Use the lines below to print a copy of the dataset for testing
    ##Results Table Date in results_data.py
    #print('results_raw_data =', df.to_dict(orient='list'))
    #print('results_df = pd.DataFrame(results_raw_data, columns = ' + str(list(df)) + ')')

    ##Convert date column to datetime using format YYYY-MM-DD
    df['Date'] = pd.to_datetime(df.Date, format='%Y%m%d', errors='ignore')

    ##Filter All Players
    game_stats = df.filter(['Date','Team A Result?','Team B Result?'])
    ##Take only the last 10 games
    game_stats = game_stats.tail(10)
    ##Sort by date
    game_stats = game_stats.sort_values(by=['Date'],ascending=False)
    ##Convert from df to list without index to be used in forms
    game_stats = game_stats.to_records(index=False)
    game_stats = list(game_stats)

    ##Use data frame shape to work out end row
    end_row = df.shape[0] + 1
    
    ##Use iloc to get last row and columns for teama,teamb,dash and date
    ##iloc takes the row as the first value and column's' as the second value
    teama = df.iloc[-1,5:10]
    teama = list(teama)
    teamb = df.iloc[-1,10:15]
    teamb = list(teamb)
    dash = df.iloc[-1,1]
    date = df.iloc[-1,0]
    return end_row,teama,teamb,dash,date,game_stats