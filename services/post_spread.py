from services.get_date import next_wednesday
from services.get_spread import wsp, wsr, player

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
    print("Wiping tally!")
    return update_tally(game_player_clear)

def sort_players():
    '''Sorts players A to Z by Name'''
    col = wsp.find('Name')
    wsp.sort((col.col, 'asc'), range='A2:P1000')
    print("Sorting Player Names!")
    return

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
    row = wsr.find('-')
    row = row.row
    col = wsr.find('Team A Result?')
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+str(row) #Put col letter with row number
    values = [values, []] #Update func expecting list of lists
    return wsr.update(range, values, major_dimension='ROWS')

def update_scorea(value):
    '''Function to update the result using the values from the results page
    Takes in value to be added to sheet and returns the gspread command for updating cell'''
    row = wsr.find('-')
    col = wsr.find('Team A Result?')
    return wsr.update_cell(row.row, col.col, value)

def update_scoreb(value):
    '''Function to update the result using the values from the results page
    Takes in value to be added to sheet and returns the gspread command for updating cell'''
    row = wsr.find('-')
    col = wsr.find('Team B Result?')
    return wsr.update_cell(row.row, col.col, value)

def update_playing_status(player):
    '''Takes in a player 
    and adds x into the playing column'''
    cell_name = wsp.find(player) #Find the Players name and the row
    clm_playing = wsp.find('Playing') #Find the Playing column
    wsp.update_cell(cell_name.row, clm_playing.col, 'x')
    print("Updated playing status for:",player)
    return

def swap_player(player):
    '''Takes in a list of two players
    finds their score and swaps them in the results table'''

    player_current = wsp.find(player[0]) #Find the Current Players name and the row
    player_new = wsp.find(player[1]) #Find the New Players name and the row
    clm_total = wsp.find('Total') #Find the Total column
    clm_total = colnum_string(clm_total.col) #Convert Total Col Number to a Letter
    player_current_range = str(clm_total)+str(player_current.row) #Combine Col letter and row num into range
    player_new_range = str(clm_total)+str(player_new.row) #Combine Col letter and row num into range
    player_current_score = wsp.acell(player_current_range).value #Grab score cell using range
    player_new_score = wsp.acell(player_new_range).value #Grab score cell using range
    player_score_difference = int(player_current_score) - int(player_new_score) #Work out difference between player scores
    print(f"The difference between player scores is {player_score_difference}")
    row = wsr.find('-') #Find the row with dash
    player_current = wsr.find(player[0], in_row=row.row) #Find the Current Players name on the row with a dash

    if player_current.col > 10 : #If player col number > 10 E.g. above J then team is B
        team = "B"
    else:
        team = "A"

    col_result_num = wsr.find('Team ' + team + ' Total') #Find the column with the score from Team A or B
    col_result = colnum_string(col_result_num.col) #Convert Col Number to a Letter
    team_result_range = str(col_result)+str(row.row) #Combine Col letter and row num into range
    team_result = wsr.acell(team_result_range).value #Grab current score for Team A or B
    new_result = int(team_result) - player_score_difference #New Result is current result minus difference

    ##Update cell with new score,
    ##using the row with the dash,
    ##and column with Team Result
    wsr.update_cell(row.row, col_result_num.col, new_result)

    ##Update cell with new player,
    ##using the row with the dash,
    ##and column with Player Current
    wsr.update_cell(row.row, player_current.col, player[1])

    print("Swapped player and updated score")
    return

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
    clm_played = wsp.find('Played')
    clm_percent = wsp.find('Percent Calc')
    clm_percent3 = wsp.find('Win Percentage')
    wins_formula = '=SUM(SUMPRODUCT((Results!$F$2:$J$929 = $A{})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))+(SUMPRODUCT((Results!$K$2:$O$929 = $A{})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))'.format(cell_name.row,cell_name.row)
    draws_formula = '=SUM(SUMPRODUCT((Results!$F$2:$O$929 = $A{})*(Results!$B$2:$B$929=Results!$C$2:$C$929)))'.format(cell_name.row)
    losses_formula = '=SUM(SUMPRODUCT((Results!$F$2:$J$929 = $A{})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))+(SUMPRODUCT((Results!$K$2:$O$929 = $A{})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))'.format(cell_name.row,cell_name.row)
    score_formula = '=IFERROR((C{}*3+D{}),0)'.format(cell_name.row,cell_name.row)
    played_formula = '=C{}+D{}+E{}'.format(cell_name.row,cell_name.row,cell_name.row)
    percent_formula = '=IFERROR((C{}/H{}*100),0)'.format(cell_name.row,cell_name.row)
    percent3_formula = '=IF(H{}<3,0,I{})'.format(cell_name.row,cell_name.row)
    wsp.update_cell(cell_name.row,clm_wins.col,wins_formula)
    wsp.update_cell(cell_name.row,clm_draws.col,draws_formula)
    wsp.update_cell(cell_name.row,clm_losses.col,losses_formula)
    wsp.update_cell(cell_name.row,clm_score.col,score_formula)
    wsp.update_cell(cell_name.row,clm_playing.col,'o')
    wsp.update_cell(cell_name.row,clm_played.col,played_formula)
    wsp.update_cell(cell_name.row,clm_percent.col,percent_formula)
    wsp.update_cell(cell_name.row,clm_percent3.col,percent3_formula)
    print("Updated Formulas!")
    return