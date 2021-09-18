from services.get_date import next_wednesday
from services.get_spread import ws_players, ws_results, player

def colnum_string(n):
    '''Converts a number column value 
    into a letter column value
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
    col = ws_players.find('Name')
    ws_players.sort((col.col, 'asc'), range='A2:P1000')
    print("Sorting Player Names!")
    return

def update_result(values):
    '''Function to update the result row 
    using the values from the results page
    Takes in values to be added to sheet and 
    returns the gspread command for updating row
    https://stackoverflow.com/questions/59701452/how-to-update-cells-in-a-google-spreadsheet-with-python-s-gspread-wks-update-cel'''
    #Find the cell containing next wednesdays date
    cell = ws_results.find(next_wednesday) 
    row = cell.row
    col = colnum_string(cell.col) #Convert col number to letter
    range = str(col)+str(row) #Put col letter with row number
    values = [values, []] #Update func expecting list of lists
    ws_results.update(range, 
                      values, 
                      major_dimension='ROWS', 
                      value_input_option='USER_ENTERED')
    #Wipe tally once teams posted to the results page
    return wipe_tally() 

def update_tally(values):
    '''Function to update the player 
    tally using the values from the index page
    Takes in values to be added as a list 
    to sheet and returns the gspread command 
    for updating the cell'''
    col = ws_players.find('Playing')
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+'2'
    values = [values, []] #Update func expecting list of lists
    return ws_players.update(range, values, major_dimension='COLUMNS')

def append_result(values):
    '''Function to update the result 
    using the values from the results page
    Takes in values to be added to sheet 
    and returns the gspread command for 
    appending the row'''
    ws_results.append_row(values, 
                          value_input_option='USER_ENTERED')
    return wipe_tally() #Wipe tally once teams posted to the results page

def update_score_result(values):
    '''Function to update the result using 
    the values from the results page
    Takes in values to be added to sheet and 
    returns the gspread command for updating row
    Updates both Score A and Score B 
    from a list of two values.'''
    row = ws_results.find('-')
    row = row.row
    col = ws_results.find('Team A Result?')
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+str(row) #Put col letter with row number
    values = [values, []] #Update func expecting list of lists
    return ws_results.update(range, values, major_dimension='ROWS')

def update_scorea(value):
    '''Function to update the result using 
    the values from the results page
    Takes in value to be added to sheet and 
    returns the gspread command for updating cell'''
    row = ws_results.find('-')
    col = ws_results.find('Team A Result?')
    return ws_results.update_cell(row.row, col.col, value)

def update_scoreb(value):
    '''Function to update the result using 
    the values from the results page
    Takes in value to be added to sheet and 
    returns the gspread command for updating cell'''
    row = ws_results.find('-')
    col = ws_results.find('Team B Result?')
    return ws_results.update_cell(row.row, col.col, value)

def update_playing_status(player):
    '''Takes in a player 
    and adds x into the playing column'''
    cell_name = ws_players.find(player) #Find the Players name and the row
    clm_playing = ws_players.find('Playing') #Find the Playing column
    ws_players.update_cell(cell_name.row, clm_playing.col, 'x')
    print("Updated playing status for:",player)
    return

def swap_player(player):
    '''Takes in a list of two players
    finds their score and swaps them 
    in the results table'''

    #Find the Current Players name and the row
    player_current = ws_players.find(player[0])

    #Find the New Players name and the row
    player_new = ws_players.find(player[1]) 

    #Find the Total column
    clm_total = ws_players.find('Total')

    #Convert Total Col Number to a Letter
    clm_total = colnum_string(clm_total.col) 

    #Combine Col letter and row num into range
    player_current_range = str(clm_total)+str(player_current.row)

    #Combine Col letter and row num into range
    player_new_range = str(clm_total)+str(player_new.row) 

    #Grab score cell using range
    player_current_score = ws_players.acell(player_current_range).value 

    #Grab score cell using range
    player_new_score = ws_players.acell(player_new_range).value 

    #Work out difference between player scores
    player_score_difference = int(player_current_score) \
                                  - int(player_new_score)

    print(f"The difference between player \
        scores is {player_score_difference}")
    row = ws_results.find('-') #Find the row with dash

    #Find the Current Players name on the row with a dash
    player_current = ws_results.find(player[0], in_row=row.row) 

#If player col number > 10 E.g. above J then team is B  
    if player_current.col > 10 : 
        team = "B"
    else:
        team = "A"

    #Find the column with the score from Team A or B
    col_result_num = ws_results.find('Team ' + team + ' Total') 

    #Convert Col Number to a Letter
    col_result = colnum_string(col_result_num.col) 

    #Combine Col letter and row num into range
    team_result_range = str(col_result)+str(row.row) 

    #Grab current score for Team A or B
    team_result = ws_results.acell(team_result_range).value 

    #New Result is current result minus difference
    new_result = int(team_result) - player_score_difference 

    ##Update cell with new score,
    ##using the row with the dash,
    ##and column with Team Result
    ws_results.update_cell(row.row, col_result_num.col, new_result)

    ##Update cell with new player,
    ##using the row with the dash,
    ##and column with Player Current
    ws_results.update_cell(row.row, player_current.col, player[1])

    print("Swapped player and updated score")
    return

def modify_playing_status(player):
    '''Takes in a player
    and adds o into the playing column'''

    #Find the Players name and the row
    cell_name = ws_players.find(player) 

    #Find the Playing column
    clm_playing = ws_players.find('Playing') 

    ws_players.update_cell(cell_name.row, 
                           clm_playing.col, 
                           'o')
    print("Modified playing status for:",player)
    return

def add_new_player(player):
    '''Appends New Row with a new 
    player and generic score'''

    #Add generic score to playername
    new_player = [player,int(77)] 

    #Should be a list of name and score
    ws_players.append_row(new_player) 
    print("Appended new row for:",new_player)

    #Run the copy formulas func using first element of list as name
    return copy_formulas(new_player[0]) 

def remove_player(player):
    '''Appends New Row with a new 
    player and generic score
    Expects two items in a list, Name and Score'''
    cell_name = ws_players.find(player)
    ws_players.delete_row(cell_name.row)
    print("Deleted row for:",player)
    return

def copy_formulas(player):
    '''Updates formulas for new players'''
    cell_name = ws_players.find(player)
    row = cell_name.row
    clm_wins = ws_players.find('Wins')
    clm_draws = ws_players.find('Draws')
    clm_losses = ws_players.find('Losses')
    clm_score = ws_players.find('Score')
    clm_playing = ws_players.find('Playing')
    clm_played = ws_players.find('Played')
    clm_percent = ws_players.find('Percent Calc')
    clm_percent3 = ws_players.find('Win Percentage')
    wins_formula = f'=SUM(SUMPRODUCT((Results!$F$2:$J$929 \
                     = $A{row})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))\
                     +(SUMPRODUCT((Results!$K$2:$O$929 \
                     = $A{row})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))'
    draws_formula = f'=SUM(SUMPRODUCT((Results!$F$2:$O$929 \
                      = $A{row})*(Results!$B$2:$B$929=Results!$C$2:$C$929)))'
    losses_formula = f'=SUM(SUMPRODUCT((Results!$F$2:$J$929 \
                       = $A{row})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))\
                       +(SUMPRODUCT((Results!$K$2:$O$929 \
                       = $A{row})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))'
    score_formula = f'=IFERROR((C{row}*3+D{row}),0)'
    played_formula = f'=C{row}+D{row}+E{row}'
    percent_formula = f'=IFERROR((C{row}/H{row}*100),0)'
    percent3_formula = f'=IF(H{row}<3,0,I{row})'
    ws_players.update_cell(row,
                           clm_wins.col,
                           wins_formula)
    ws_players.update_cell(row,
                           clm_draws.col,
                           draws_formula)
    ws_players.update_cell(row,
                           clm_losses.col,
                           losses_formula)
    ws_players.update_cell(row,
                           clm_score.col,
                           score_formula)
    ws_players.update_cell(row,
                           clm_playing.col,
                           'o')
    ws_players.update_cell(row,
                           clm_played.col,
                           played_formula)
    ws_players.update_cell(row,
                           clm_percent.col,
                           percent_formula)
    ws_players.update_cell(row,
                           clm_percent3.col,
                           percent3_formula)
    print("Updated Formulas!")
    return