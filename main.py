from flask import Flask, render_template, request
from player import *
app = Flask(__name__)

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
        # Sort game_players by the key of the second column
        game_players.sort(key=lambda x:x[1])
        # Put the Even elements from the array starting from zero
        # and counting in twos into Team A
        team_a = game_players[0::2]
        # Put the Odd elements from the array starting from 1 
        # and counting in twos into Team B
        team_b = game_players[1::2]
        team_a = ([row[0] for row in team_a])
        team_b = ([row[0] for row in team_b])
        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a, teamb = team_b)
    # If request method is not POST then reload back to index.html
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000)