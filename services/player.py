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
all_players.append( Player(1,'Chris',17,17,12,18,15) )
all_players.append( Player(2,'Gavin',19,18,14,17,19) )
all_players.append( Player(3,'Pete',16,14,13,16,19) )
all_players.append( Player(4,'Kevin',16,11,12,15,17) )
all_players.append( Player(5,'Ferdi',16,11,10,16,18) )
all_players.append( Player(6,'Cal',14,11,10,12,9) )
all_players.append( Player(7,'Tom',12,9,10,11,10) )
all_players.append( Player(8,'Joe',14,15,18,17,18) )
all_players.append( Player(9,'Simon',12,15,19,14,9) )
all_players.append( Player(10,'Rik',12,19,10,14,12) )
all_players.append( Player(11,'James',14,17,11,11,15) )
all_players.append( Player(12,'Phil',18,17,11,15,18) )
all_players.append( Player(13,'Dida',17,15,20,15,19) )
all_players.append( Player(14,'Rich',17,17,18,15,19) )
all_players.append( Player(15,'Bernard',16,15,16,13,9) )
all_players.append( Player(16,'Matt',11,11,9,9,7) )
all_players.append( Player(17,'Will',9,9,13,9,7) )
all_players.append( Player(18,'Level1',11,11,9,9,7) )
all_players.append( Player(19,'Level2',14,11,10,12,9) )
all_players.append( Player(20,'Level3',16,11,12,15,17) )
all_players.append( Player(21,'Level4',19,18,14,17,19) )

player_names = []
for obj in all_players: 
    player_names.append((obj.name))
player_names.sort()