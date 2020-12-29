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