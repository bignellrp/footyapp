from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys, heapq
sys.dont_write_bytecode = True
from flask import Flask, render_template, request
from player import all_players, player_names
app = Flask(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
SAMPLE_RANGE_NAME = 'Sheet2!A2:F'
WRITE_SAMPLE_RANGE_NAME = 'Sheet3!A1:AA1000'

#Start the Web Form for pulling the checkbox data input
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
        print(request.form.getlist('available_players'))
    
        # Use GetList to put the data from the index template into the array
        available_players = []
        available_players = request.form.getlist('available_players')

        # Define game_players array for storing the players names 
        # and scores only if the names are listed in available_players
        game_players = []
        for obj in all_players: 
            if obj.name in available_players:
                game_players.append((obj.name , obj.score))
        
        #print (game_players)

        # Sort game_players by the key of the second column
        game_players.sort(key=lambda x:x[1])
        # Put the Even elements from the array starting from zero
        # and counting in twos into Team A
        team_a = game_players[0::2]
        # Put the Odd elements from the array starting from 1 
        # and counting in twos into Team B
        team_b = game_players[1::2]
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
                    pickle.dump(creds, token)
            service = build('sheets', 'v4', credentials=creds)
            print (game_players)
            body = {
                'majorDimension': 'ROWS',
                'values': team_a
                }
            result = service.spreadsheets().values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=WRITE_SAMPLE_RANGE_NAME,
                valueInputOption='USER_ENTERED', body=body).execute()
            print('{0} cells updated.'.format(result.get('updatedCells')))
        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    return render_template('index.html', player_names = player_names)

#Start the Compare Web Form for pulling the checkbox data input
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST': 
        print(request.form.getlist('available_players_a'))
        print(request.form.getlist('available_players_b'))
        # Use GetList to put the data from the index template into the array
        available_players_a = []
        available_players_a = request.form.getlist('available_players_a')
        available_players_b = []
        available_players_b = request.form.getlist('available_players_b')
        # Define game_players array for storing the players names 
        # and scores only if the names are listed in available_players
        game_players_a = []
        for obj in all_players: 
            if obj.name in available_players_a:
                game_players_a.append((obj.score))
        
        game_players_b = []
        for obj in all_players: 
            if obj.name in available_players_b:
                game_players_b.append((obj.score))
        # Sum of the total score from second column
        team_a_result = (sum(game_players_a))
        team_b_result = (sum(game_players_b))
        # Return results to result_compare.html template
        return render_template('result_compare.html', teamares = team_a_result, teambres = team_b_result)
    # If request method is not POST then it must be GET so render compare.html including player_names
    return render_template('compare.html', player_names = player_names)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000)
