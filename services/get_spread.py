import gspread
import pandas as pd
from services.lookup import lookup
from services.get_oscommand import GITBRANCH, IFBRANCH

SERVICE_ACCOUNT_FILE = './services/keys.json'
TOKEN_FILE = './services/tokens.json'
SPREADSHEET_ID = lookup("SPREADSHEET_ID")

gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
ss = gc.open_by_key(SPREADSHEET_ID)

if IFBRANCH in GITBRANCH:
    print("Using Dev Worksheet for Get Commands")
    wsp = ss.worksheet('Dev Players')
    wsr = ss.worksheet('Dev Results')
else:
    print("Using Pro Worksheet for Get Commands")
    wsp = ss.worksheet('Players')
    wsr = ss.worksheet('Results')

class player():
	
    def __init__(self):
        ##Initialise the class and get all the values from the players sheet
        players_table = wsp.get_all_values()
        self.df = pd.DataFrame(players_table[1:], columns=players_table[0])
        ##Sort df values by name to hide what score players have
        ##Otherwise best players would show at the top
        self.df = self.df.sort_values(by=['Name'],ascending=True)

    def player_names(self):
        ##Filter Names and convert to list
        self.player_names = self.df.filter(['Name','Playing'])
        ##Convert from df to list without index to be used in forms
        self.player_names = self.player_names.to_records(index=False)
        self.player_names = list(self.player_names)
        return self.player_names
		
    def all_players(self):
        ##Filter All Players
        self.all_players = self.df.filter(['Name','Total'])
        ##Convert Total column to numeric so they can be added up
        self.all_players['Total'] = pd.to_numeric(self.all_players['Total'])
        ##Convert from df to list without index to be used in forms
        self.all_players = self.all_players.to_records(index=False)
        self.all_players = list(self.all_players)
        return self.all_players

    def player_stats(self):
        ##Filter Player Stats
        self.player_stats = self.df.filter(['Name','Wins','Draws','Losses','Score'])
        ##Convert multiple columns to numeric
        self.player_stats[['Wins','Draws','Losses','Score']] = self.player_stats[['Wins','Draws','Losses','Score']].apply(pd.to_numeric)
        ##Sort by Score
        self.player_stats = self.player_stats.sort_values(by=['Score'],ascending=False)
        ##Convert from df to list without index to be used in forms
        self.player_stats = self.player_stats.to_records(index=False)
        self.player_stats = list(self.player_stats)
        return self.player_stats

    def leaderboard(self):
        ##Filter Game Stats for Leaderboard
        self.leaderboard = self.df.filter(['Name','Score'])
        ##Convert Score column to numeric so they can be added up
        self.leaderboard['Score'] = pd.to_numeric(self.leaderboard['Score'])
        self.leaderboard = self.leaderboard.sort_values(by=['Score'],ascending=False)
        ##Head the top10
        self.leaderboard = self.leaderboard.head(10)
        ##Convert from df to list without index to be used in forms
        self.leaderboard = self.leaderboard.to_records(index=False)
        self.leaderboard = list(self.leaderboard)
        return self.leaderboard

    def player_count(self):
        ##Count the number of players in tally
        game_tally = []
        game_player_tally = []
        player_names = self.df.filter(['Name','Playing'])
        ##Convert from df to list without index to be used in forms
        player_names = player_names.to_records(index=False)
        player_names = list(player_names)
        for row in player_names:
            '''Takes in row of player_names
            and outputs a just the tally column'''
            game_player_tally.append((row[0]))
            game_tally.append((row[1]))
        self.player_count = 10 - game_tally.count("x")
        return self.player_count
    
    def game_player_tally(self):
        ##List of player names playing
        game_player_tally = []
        player_names = self.df.filter(['Name','Playing'])
        ##Convert from df to list without index to be used in forms
        player_names = player_names.to_records(index=False)
        player_names = list(player_names)
        for row in player_names:
            '''Takes in row of player names 
            and returns a tally of those players
            that are available this week'''
            if row[1] == "x":
                game_player_tally.append((row[0]))
        self.game_player_tally = game_player_tally
        return self.game_player_tally

    def game_player_tally_with_score(self):
        ##List of player names playing
        game_player_tally = []
        player_names = self.df.filter(['Name','Total','Playing'])
        ##Convert from df to list without index to be used in forms
        player_names = player_names.to_records(index=False)
        player_names = list(player_names)
        for row in player_names:
            '''Takes in row of player names 
            and returns a tally of those players
            that are available this week'''
            if row[2] == "x":
                game_player_tally.append((row[0] , int(row[1])))
        self.game_player_tally_with_score = game_player_tally
        return self.game_player_tally_with_score

class results():

    def __init__(self):
        ##Initialise the class and get all the values from the results sheet
        results_table = wsr.get_all_values()
        ##Add values to data frame
        self.df = pd.DataFrame(results_table[1:], columns=results_table[0])
        ##Convert date column to datetime using format YYYY-MM-DD
        self.df['Date'] = pd.to_datetime(self.df.Date, format='%Y%m%d', errors='ignore')
    
    def game_stats(self):
        ##Filter All Players
        self.game_stats = self.df.filter(['Date','Team A Result?','Team B Result?'])
        ##Take only the last 10 games
        self.game_stats = self.game_stats.tail(10)
        ##Sort by date
        self.game_stats = self.game_stats.sort_values(by=['Date'],ascending=False)
        ##Convert from df to list without index to be used in forms
        self.game_stats = self.game_stats.to_records(index=False)
        self.game_stats = list(self.game_stats)
        return self.game_stats
    
    def teama(self):
        ##Use iloc to get last row and columns for teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value and column's' as the second value
        self.teama = self.df.iloc[-1,5:10]
        self.teama = list(self.teama)
        return self.teama

    def teamb(self):
        ##Use iloc to get last row and columns for teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value and column's' as the second value
        self.teamb = self.df.iloc[-1,10:15]
        self.teamb = list(self.teamb)
        return self.teamb

    def scorea(self):
        ##Use iloc to get last row and columns for teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value and column's' as the second value
        self.scorea = self.df.iloc[-1,1]
        return self.scorea
    
    def scoreb(self):
        ##Use iloc to get last row and columns for teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value and column's' as the second value
        self.scoreb = self.df.iloc[-1,2]
        return self.scoreb

    def date(self):
        ##Use iloc to get last row and columns for teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value and column's' as the second value
        self.date = self.df.iloc[-1,0]
        return self.date