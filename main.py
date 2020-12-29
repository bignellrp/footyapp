from flask import Flask, render_template, request
app = Flask(__name__)

# Define the Player Structure into Class Player
class Player:
    def __init__(self, number, name, speed, stamina, goalkeeping, defense, offense):
        self.number = number
        self.name = name
        self.speed = speed
        self.stamina = stamina
        self.goalkeeping = goalkeeping
        self.defense = defense
        self.offense = offense
        self.score = speed + stamina + goalkeeping + defense + offense

# Enter the Player Data into an array called all_players
all_players = []
all_players.append( Player(1, 'Pete', 8, 3, 7, 3, 9) )
all_players.append( Player(2, 'Simon', 6, 7, 9, 8, 2) )
all_players.append( Player(3, 'Rik', 6, 8, 2, 2, 2) )
all_players.append( Player(4, 'Chris', 8, 7, 4, 5, 7) )
all_players.append( Player(5, 'Joe', 9, 7, 7, 7, 10) )
all_players.append( Player(6, 'Darren', 4, 3, 6, 6, 6) )
all_players.append( Player(7, 'Ferdi', 7, 3, 3, 5, 9) )
all_players.append( Player(8, 'Rich', 7, 7, 7, 8, 9) )
all_players.append( Player(9, 'Tom', 3, 8, 4, 4, 4) )
all_players.append( Player(10, 'Cal', 5, 5, 5, 5, 5) )
all_players.append( Player(11, 'Dida', 7, 7, 7, 8, 9) )
all_players.append( Player(12, 'Matt', 2, 3, 5, 6, 4) )
all_players.append( Player(13, 'Bernard', 5, 6, 5, 9, 4) )
all_players.append( Player(14, 'Phil', 8, 7, 3, 8, 9) )
all_players.append( Player(15, 'Kev', 4, 5, 6, 7, 8) )
all_players.append( Player(16, 'Will', 3, 4, 5, 5, 5) )
all_players.append( Player(17, 'Level1', 1, 2, 2, 2, 2) )
all_players.append( Player(18, 'Level2', 3, 3, 3, 3, 3) )
all_players.append( Player(19, 'Level3', 6, 6, 6, 6, 6) )
all_players.append( Player(20, 'Level4', 9, 9, 9, 9, 9) )

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