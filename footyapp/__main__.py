import heapq
import os
import pickle
import sys

from flask import Flask, render_template, request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .json_date import next_wednesday


def even_teams(game_players, n=2):
    teams = [[] for _ in range(n)]
    totals = [(0, i) for i in range(n)]
    heapq.heapify(totals)
    for obj in game_players:
        total, index = heapq.heappop(totals)
        teams[index].append(obj)
        heapq.heappush(totals, (total + obj[1], index))
    return tuple(teams)

app = Flask(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
RANGE_NAME = 'Sheet2!A2:G'
WRITE_RANGE_NAME = 'Sheet3!A1:AA1000'

creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
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
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token, protocol=2)
SERVICE = build('sheets', 'v4', credentials=creds)

def _fetch_sheet():

    sheet = SERVICE.spreadsheets()
    return sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
def _make_players(sheet_values):
    values = sheet_values.get('values', [])
    player_names = ([row[0] for row in values])
    all_players = []
    class Player:
        def __init__(self, name, score):
            self.name = name
            self.score = score
    for row in values:
        all_players.append( Player( row[0], row[6] ))
    return all_players, player_names


@app.route('/', methods=['GET', 'POST'])
def index():
    """Start the Web Form for pulling the checkbox data input"""
    all_players, player_names = _make_players(_fetch_sheet())
    if request.method == 'POST':

        # Use GetList to put the data from the index template into the array
        available_players = []
        available_players = request.form.getlist('available_players')

        # Define game_players array for storing the players names 
        # and scores only if the names are listed in available_players
        game_players = []
        for obj in all_players:
            if obj.name in available_players:
                game_players.append((obj.name , int(obj.score)))

        # Add the even teams into team a and team b
        team_a, team_b = even_teams(game_players)

        # Take the first column and put names into team_a and team_b
        team_a_names = ([row[0] for row in team_a])
        team_b_names = ([row[0] for row in team_b])

        # Calculate the score
        team_a_score = ([row[1] for row in team_a])
        team_b_score = ([row[1] for row in team_b])

        # Sum the total of the scores
        team_a_total = (sum(team_a_score))
        team_b_total = (sum(team_b_score))

        # Post Results to Google Sheets if output is checked
        output_checked = []
        output_checked = request.form.getlist('output_checked')
        if output_checked == ['Yes']:
            # Format the google ouput into one long comma sep str
            google_output = []
            google_output.append((next_wednesday))
            google_output.append(("TeamAResult?"))
            google_output.append(("TeamBResult?"))
            google_output.append((team_a_total))
            google_output.append((team_b_total))
            for obj in team_a_names: 
                google_output.append((obj))
            for obj in team_b_names: 
                google_output.append((obj))
            # Format the google body for ROWS
            body = {
                'majorDimension': 'ROWS',
                'values': [
                    google_output,
                ],
                }
            # Print the result to google sheets with append enabled
            result = SERVICE.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID, range=WRITE_RANGE_NAME,
                valueInputOption='USER_ENTERED', body=body).execute()
        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    return render_template('index.html', player_names=player_names)

#Start the Compare Web Form for pulling the checkbox data input
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    all_players, player_names = _make_players(_fetch_sheet())
    if request.method == 'POST':
        # Use GetList to put the data from the index template into the array
        available_players_a = []
        available_players_a = request.form.getlist('available_players_a')
        available_players_b = []
        available_players_b = request.form.getlist('available_players_b')
        game_players_a = []
        for obj in all_players: 
            if obj.name in available_players_a:
                game_players_a.append((obj.name , obj.score))
        game_players_b = []
        for obj in all_players: 
            if obj.name in available_players_b:
                game_players_b.append((obj.name , obj.score))
        # Take the first column and put names into team_a and team_b
        team_a = game_players_a
        team_b = game_players_b
        # Take the first column and put names into team_a and team_b
        team_a_names = ([row[0] for row in team_a])
        team_b_names = ([row[0] for row in team_b])
        # Calculate the score
        team_a_score = ([row[1] for row in team_a])
        team_b_score = ([row[1] for row in team_b])
        team_a_score = [int(i) for i in team_a_score]
        team_b_score = [int(i) for i in team_b_score]
        # Sum the total of the scores
        team_a_total = (sum(team_a_score))
        team_b_total = (sum(team_b_score))
        # Post Results to Google Sheets if output is checked
        output_checked = []
        output_checked = request.form.getlist('output_checked')
        if output_checked == ['Yes']:
            # Format the google ouput into one long comma sep str
            google_output = []
            google_output.append((next_wednesday))
            google_output.append(("TeamAResult?"))
            google_output.append(("TeamBResult?"))
            google_output.append((team_a_total))
            google_output.append((team_b_total))
            for obj in team_a_names: 
                google_output.append((obj))
            for obj in team_b_names: 
                google_output.append((obj))
            # Format the google body for ROWS
            body = {
                'majorDimension': 'ROWS',
                'values': [
                    google_output,
                ],
                }
            # Print the result to google sheets with append enabled
            result = SERVICE.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID, range=WRITE_RANGE_NAME,
                valueInputOption='USER_ENTERED', body=body).execute()
        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    # If request method is not POST then it must be GET so render compare.html including player_names
    return render_template('compare.html', player_names = player_names)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000)
