# Define the Player Structure into Class Player
class Player:
    def __init__(self, number, name, passing, stamina, goalkeeping, defense, offense):
        self.number = number
        self.name = name
        self.passing = passing
        self.stamina = stamina
        self.goalkeeping = goalkeeping
        self.defense = defense
        self.offense = offense
        self.score = passing + stamina + goalkeeping + defense + offense

# Enter the Player Data into an array called all_players
all_players = []
all_players.append( Player(1,'Player1',17,17,12,18,15) )
all_players.append( Player(2,'Player2',19,18,14,17,19) )
all_players.append( Player(3,'Player3',16,14,13,16,19) )
all_players.append( Player(4,'Player4',16,11,12,15,17) )
all_players.append( Player(5,'Player5',16,11,10,16,18) )
all_players.append( Player(6,'Player6',14,11,10,12,9) )
all_players.append( Player(7,'Player7',12,9,10,11,10) )
all_players.append( Player(8,'Player8',14,15,18,17,18) )
all_players.append( Player(9,'Player9',12,15,19,14,9) )
all_players.append( Player(10,'Player10',12,19,10,14,12) )
all_players.append( Player(11,'Player11',14,17,11,11,15) )
all_players.append( Player(12,'Player12',18,17,11,15,18) )
all_players.append( Player(13,'Player13',17,15,20,15,19) )
all_players.append( Player(14,'Player14',17,17,18,15,19) )
all_players.append( Player(15,'Player15',16,15,16,13,9) )
all_players.append( Player(16,'Player16',11,11,9,9,7) )
all_players.append( Player(17,'Player17',9,9,13,9,7) )
all_players.append( Player(18,'Player18',11,11,9,9,7) )
all_players.append( Player(19,'Player19',14,11,10,12,9) )
all_players.append( Player(20,'Player20',16,11,12,15,17) )

player_names = []
for obj in all_players: 
    player_names.append((obj.name))
player_names.sort()