import gspread
import pandas as pd
from services.lookup import lookup
from services.get_oscommand import GITBRANCH, IFBRANCH
import sqlite3
from sqlite3 import Error

SERVICE_ACCOUNT_FILE = '../tokens/keys.json'
SPREADSHEET_ID = lookup("SPREADSHEET_ID")
DATABASE = '../tokens/database.db'
sql_create_players_table = '''  CREATE TABLE IF NOT EXISTS "players" (
                                    "Name"	TEXT,
                                    "Total"	INTEGER,
                                    "Wins"	INTEGER,
                                    "Draws"	INTEGER,
                                    "Losses"	INTEGER,
                                    "Score"	INTEGER,
                                    "Playing"	TEXT,
                                    "Played"	INTEGER,
                                    "Percent Calc"	INTEGER,
                                    "Win Percentage"	INTEGER
                                ); '''
sql_create_results_table = '''  CREATE TABLE "results" (
                                    "Date"	TEXT,
                                    "Team A Result?"	INTEGER,
                                    "Team B Result?"	INTEGER,
                                    "Team A Total"	INTEGER,
                                    "Team B Total"	INTEGER,
                                    "Team A Player 1"	TEXT,
                                    "Team A Player 2"	TEXT,
                                    "Team A Player 3"	TEXT,
                                    "Team A Player 4"	TEXT,
                                    "Team A Player 5"	TEXT,
                                    "Team B Player 1"	TEXT,
                                    "Team B Player 2"	TEXT,
                                    "Team B Player 3"	TEXT,
                                    "Team B Player 4"	TEXT,
                                    "Team B Player 5"	TEXT,
                                    "Team A Colour"	TEXT,
                                    "Team B Colour"	TEXT
                                ); '''
# gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
# ss = gc.open_by_key(SPREADSHEET_ID)

# if IFBRANCH in GITBRANCH:
#         print("Using Pro Worksheet for Get Commands")
#         ws_players = ss.worksheet('Players')
#         ws_results = ss.worksheet('Results')
# else:
#         print("Using Dev Worksheet for Get Commands")
#         ws_players = ss.worksheet('Dev Players')
#         ws_results = ss.worksheet('Dev Results')

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


#conn = sqlite3.connect('../tokens/database.db', check_same_thread=False)
#c = conn.cursor()

conn = create_connection(DATABASE)
c = conn.cursor()
# get the count of tables with the name  
tablename = 'players' 
c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ", (tablename, ))
fetch = c.fetchone() # this SHOULD BE in a tuple containing count(name) integer.

# check if the db has existing table names players
# if the count is 1, then table exists 
if fetch[0] == 1 : 
    print('Table exists, starting app!')
    pass
else:

    # create projects table
    create_table(conn, sql_create_players_table)
    players_table = pd.read_csv('../tokens/players.csv')
    players_table.to_sql('players', conn, if_exists='fail', index = False)
    print("Creating players table from csv.")

    # create results table
    create_table(conn, sql_create_results_table)
    results_table = pd.read_csv('../tokens/results.csv')
    results_table.to_sql('results', conn, if_exists='fail', index = False)
    print("Creating results table from csv.")
    conn.commit()


class player():
	
    def __init__(self):
        ##Initialise the class and get all the values from the players sheet
        #players_table = ws_players.get_all_values()
        #self.df = pd.DataFrame(players_table[1:], columns=players_table[0])
        self.df = pd.read_sql('''SELECT * FROM players''', conn)
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
        self.player_stats = self.df.filter(
                ['Name','Wins','Draws','Losses','Score','Win Percentage'])
        ##Convert multiple columns to numeric
        self.player_stats[['Wins','Draws',
                           'Losses','Score',
                           'Win Percentage']] = self.player_stats[['Wins',
                           'Draws','Losses','Score',
                           'Win Percentage']].apply(pd.to_numeric)
        ##Sort by Score
        self.player_stats = self.player_stats.sort_values(by=['Score'],
                                                          ascending=False)
        ##Convert from df to list without index to be used in forms
        self.player_stats = self.player_stats.to_records(index=False)
        self.player_stats = list(self.player_stats)
        return self.player_stats

    def leaderboard(self):
        ##Filter Game Stats for Leaderboard
        self.leaderboard = self.df.filter(['Name','Score'])
        ##Convert Score column to numeric so they can be added up
        self.leaderboard['Score'] = pd.to_numeric(self.leaderboard['Score'])
        self.leaderboard = self.leaderboard.sort_values(by=['Score'],
                                                        ascending=False)
        ##Head the top10
        self.leaderboard = self.leaderboard.head(10)
        ##Convert from df to list without index to be used in forms
        self.leaderboard = self.leaderboard.to_records(index=False)
        self.leaderboard = list(self.leaderboard)
        return self.leaderboard

    def winpercentage(self):
        ##Filter Game Stats for winpercentage
        self.winpercentage = self.df.filter(['Name','Win Percentage'])
        ##Convert Score column to numeric so they can be added up
        self.winpercentage['Win Percentage'] = pd.to_numeric(
                self.winpercentage['Win Percentage'])
        self.winpercentage = self.winpercentage.sort_values(
                by=['Win Percentage'],ascending=False)
        ##Head the top10
        self.winpercentage = self.winpercentage.head(10)
        ##Convert from df to list without index to be used in forms
        self.winpercentage = self.winpercentage.to_records(index=False)
        self.winpercentage = list(self.winpercentage)
        return self.winpercentage

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
    
    def game_player_tally_with_index(self):
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
        self.game_player_tally_with_index = enumerate(game_player_tally, 
                                                      start=1)
        return self.game_player_tally_with_index

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

    def game_player_tally_with_score_and_index(self):
        ##List of player names playing
        game_player_tally = []
        player_names = self.df.filter(['Name','Total','Playing'])
        ##Convert from df to list without index to be used in forms
        player_names = player_names.to_records(index=False)
        player_names = list(player_names)
        num=1
        for row in player_names:
            '''Takes in row of player names 
            and returns a tally of those players
            that are available this week'''
            if row[2] == "x":
                game_player_tally.append((num, row[0] , int(row[1])))
                num=num+1
        self.game_player_tally_with_score_and_index = game_player_tally
        return self.game_player_tally_with_score_and_index


class results():

    def __init__(self):
        ##Initialise the class and get all the values from the results sheet
        #results_table = ws_results.get_all_values()
        ##Add values to data frame
        self.df = pd.read_sql('''SELECT * FROM results''', conn)
        #self.df = pd.DataFrame(results_table[1:], columns=results_table[0])
        ##Convert date column to datetime using format YYYY-MM-DD
        self.df['Date'] = pd.to_datetime(self.df.Date, format='%Y%m%d', 
                                         errors='ignore')
    
    def all_results(self):
        ##Get all results including column names
        self.all_results = self.df
        return self.all_results


    def game_stats(self):
        ##Filter All Players
        self.game_stats = self.df.filter(['Date','Team A Result?',
                                          'Team B Result?'])
        ##Take only the last 10 games
        self.game_stats = self.game_stats.tail(10)
        ##Sort by date
        self.game_stats = self.game_stats.sort_values(by=['Date'],
                                                      ascending=False)
        ##Convert from df to list without index to be used in forms
        self.game_stats = self.game_stats.to_records(index=False)
        self.game_stats = list(self.game_stats)
        return self.game_stats
    
    def teama(self):
        ##Use iloc to get last row and 
        ##columns for teama,
        ##teamb,scorea,scoreb and date
        ##iloc takes the row as the first 
        ##value and column's' 
        ##as the second value
        self.teama = self.df.iloc[-1,5:10]
        self.teama = list(self.teama)
        return self.teama

    def teamb(self):
        ##Use iloc to get last row and columns for teama,
        ##teamb,scorea,scoreb and date
        ##iloc takes the row as the first value and 
        ##column's' as the second value
        self.teamb = self.df.iloc[-1,10:15]
        self.teamb = list(self.teamb)
        return self.teamb

    def scorea(self):
        ##Use iloc to get last row and columns for 
        ##teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value 
        ##and column's' as the second value
        self.scorea = self.df.iloc[-1,1]
        return self.scorea
    
    def scoreb(self):
        ##Use iloc to get last row and columns for 
        ##teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value 
        ##and column's' as the second value
        self.scoreb = self.df.iloc[-1,2]
        return self.scoreb

    def date(self):
        ##Use iloc to get last row and columns for 
        ##teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value 
        # and column's' as the second value
        self.date = self.df.iloc[-1,0]
        return self.date

    def totala(self):
        ##Use iloc to get last row and columns for 
        ##teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value 
        ##and column's' as the second value
        self.totala = self.df.iloc[-1,3]
        return self.totala
    
    def totalb(self):
        ##Use iloc to get last row and columns for 
        ##teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value 
        ##and column's' as the second value
        self.totalb = self.df.iloc[-1,4]
        return self.totalb

    def coloura(self):
        ##Use iloc to get last row and columns for 
        ##teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value 
        ##and column's' as the second value
        self.coloura = self.df.iloc[-1,15]
        return self.coloura
    
    def colourb(self):
        ##Use iloc to get last row and columns for 
        ##teama,teamb,scorea,scoreb and date
        ##iloc takes the row as the first value 
        ##and column's' as the second value
        self.colourb = self.df.iloc[-1,16]
        return self.colourb