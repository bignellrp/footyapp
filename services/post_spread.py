import gspread
from services.get_date import next_wednesday
from services.get_spread import player
from services.get_oscommand import GITBRANCH

#GSPREAD Vars
SERVICE_ACCOUNT_FILE = './services/keys.json'
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U' #Move to tokens file

#GSPREAD Objects
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
ss = gc.open_by_key(SPREADSHEET_ID)

if GITBRANCH == 'botpre':
    print("Using Dev Worksheet for Post Commands")
    wsp = ss.worksheet('Dev Players')
    wsr = ss.worksheet('Dev Results')
else:
    print("Using Pro Worksheet for Post Commands")
    wsp = ss.worksheet('Dev Players')
    wsr = ss.worksheet('Dev Results')

#Fuctions

def colnum_string(n):
    '''Converts a number column value into a letter column value
    E.g. Takes in 3 and outputs C 
    https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
    print(colnum_string(3))
    #output:C'''
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def wipe_tally():
    '''Wipes the tally column for all players setting it to o'''
    players = player()
    all_players = players.all_players()
    game_player_clear = []
    for row in all_players:
        '''Takes in row of all_players 
        and appends o to every row'''
        game_player_clear.append(("o"))
    return update_tally(game_player_clear)

def update_result(values):
    '''Function to update the result row using the values from the results page
    Takes in values to be added to sheet and returns the gspread command for updating row
    https://stackoverflow.com/questions/59701452/how-to-update-cells-in-a-google-spreadsheet-with-python-s-gspread-wks-update-cel'''
    cell = wsr.find(next_wednesday) #Find the cell containing next wednesdays date
    row = cell.row
    col = colnum_string(cell.col) #Convert col number to letter
    range = str(col)+str(row) #Put col letter with row number
    values = [values, []] #Update func expecting list of lists
    wsr.update(range, values, major_dimension='ROWS', value_input_option='USER_ENTERED')
    return wipe_tally() #Wipe tally once teams posted to the results page

def update_tally(values):
    '''Function to update the player tally using the values from the index page
    Takes in values to be added as a list to sheet and returns the gspread command for updating the cell'''
    col = wsp.find('Playing')
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+'2'
    values = [values, []] #Update func expecting list of lists
    return wsp.update(range, values, major_dimension='COLUMNS')

def append_result(values):
    '''Function to update the result using the values from the results page
    Takes in values to be added to sheet and returns the gspread command for appending the row'''
    wsr.append_row(values, value_input_option='USER_ENTERED')
    return wipe_tally() #Wipe tally once teams posted to the results page

def update_score_result(values):
    '''Function to update the result using the values from the results page
    Takes in values to be added to sheet and returns the gspread command for updating row
    Updates both Score A and Score B from a list of two values.'''
    row = wsr.find(next_wednesday)
    row = row.row
    col = wsr.find('Team A Result?')
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+str(row) #Put col letter with row number
    values = [values, []] #Update func expecting list of lists
    return wsr.update(range, values, major_dimension='ROWS')

def update_scorea(value):
    '''Function to update the result using the values from the results page
    Takes in value to be added to sheet and returns the gspread command for updating cell'''
    row = wsr.find(next_wednesday)
    col = wsr.find('Team A Result?')
    return wsr.update_cell(row.row, col.col, value)

def update_scoreb(value):
    '''Function to update the result using the values from the results page
    Takes in value to be added to sheet and returns the gspread command for updating cell'''
    row = wsr.find(next_wednesday)
    col = wsr.find('Team B Result?')
    return wsr.update_cell(row.row, col.col, value)

# def update_playing_status_list(name):
#     '''Takes in a list of players 
#     and adds x into the playing column'''
#     #for name in player_list:
#     cell_name = wsp.find(name) #Find the Players name and the row
#     clm_playing = wsp.find('Playing') #Find the Playing column
#     wsp.update_cell(cell_name.row, clm_playing.col, 'x')
#     print("Updated playing status for:",name)
#     return

def update_playing_status(player):
    '''Takes in a player 
    and adds x into the playing column'''
    cell_name = wsp.find(player) #Find the Players name and the row
    clm_playing = wsp.find('Playing') #Find the Playing column
    wsp.update_cell(cell_name.row, clm_playing.col, 'x')
    print("Updated playing status for:",player)
    return

# def modify_playing_status_list(player_list):
#     '''Takes in a list of players 
#     and adds o into the playing column'''
#     for name in player_list:
#         print(name)
#         cell_name = wsp.find(name) #Find the Players name and the row
#         clm_playing = wsp.find('Playing') #Find the Playing column
#         wsp.update_cell(cell_name.row, clm_playing.col, 'o')
#         print("Modified playing status for:",name)
#     return

def modify_playing_status(player):
    '''Takes in a player
    and adds o into the playing column'''
    cell_name = wsp.find(player) #Find the Players name and the row
    clm_playing = wsp.find('Playing') #Find the Playing column
    wsp.update_cell(cell_name.row, clm_playing.col, 'o')
    print("Modified playing status for:",player)
    return

def add_new_player(player):
    '''Appends New Row with a new 
    player and generic score'''
    new_player = [player,int(77)] #Add generic score to playername
    wsp.append_row(new_player) #Should be a list of name and score
    print("Appended new row for:",new_player)
    return copy_formulas(new_player[0]) #Run the copy formulas func using first element of list as name

def remove_player(player):
    '''Appends New Row with a new 
    player and generic score
    Expects two items in a list, Name and Score'''
    cell_name = wsp.find(player)
    wsp.delete_row(cell_name.row)
    print("Deleted row for:",player)
    return

def copy_formulas(player):
    '''Updates formulas for new players'''
    cell_name = wsp.find(player)
    clm_wins = wsp.find('Wins')
    clm_draws = wsp.find('Draws')
    clm_losses = wsp.find('Losses')
    clm_score = wsp.find('Score')
    clm_playing = wsp.find('Playing')
    wins_formula = '=SUM(SUMPRODUCT((Results!$F$2:$J$929 = $A{})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))+(SUMPRODUCT((Results!$K$2:$O$929 = $A{})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))'.format(cell_name.row,cell_name.row)
    draws_formula = '=SUM(SUMPRODUCT((Results!$F$2:$O$929 = $A{})*(Results!$B$2:$B$929=Results!$C$2:$C$929)))'.format(cell_name.row)
    losses_formula = '=SUM(SUMPRODUCT((Results!$F$2:$J$929 = $A{})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))+(SUMPRODUCT((Results!$K$2:$O$929 = $A{})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))'.format(cell_name.row,cell_name.row)
    score_formula = '=IFERROR((H{}*3+I{}),0)'.format(cell_name.row,cell_name.row)
    wsp.update_cell(cell_name.row,clm_wins.col,wins_formula)
    wsp.update_cell(cell_name.row,clm_draws.col,draws_formula)
    wsp.update_cell(cell_name.row,clm_losses.col,losses_formula)
    wsp.update_cell(cell_name.row,clm_score.col,score_formula)
    wsp.update_cell(cell_name.row, clm_playing.col, 'o')
    print("Updated Formulas!")
    return