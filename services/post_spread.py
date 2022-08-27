from services.get_date import next_wednesday
#from services.get_spread import ws_players, ws_results, player, conn
from services.get_spread import player,results, conn

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
    #players = player()
    #all_players = players.all_players()
    #game_player_clear = []
    #for row in all_players:
    #    '''Takes in row of all_players 
    #    and appends o to every row'''
    #    game_player_clear.append(("o"))
    sql = '''   UPDATE players 
                SET "Playing"="o";'''
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    print("Wiping tally!")
    #return update_tally(game_player_clear)
    return update_all_formulas()

def sort_players():
    '''Sorts players A to Z by Name'''
    #col = ws_players.find('Name')
    #ws_players.sort((col.col, 'asc'), range='A2:P1000')
    sql = '''SELECT * FROM players ORDER BY Name COLLATE NOCASE ASC;'''
    c = conn.cursor()
    c.execute(sql)
    print("Sorting Player Names!")
    return

def update_result(values):
    '''Function to update the result row 
    using the values from the results page
    Takes in values to be added to sheet and 
    returns the gspread command for updating row
    https://stackoverflow.com/questions/59701452/how-to-update-cells-in-a-google-spreadsheet-with-python-s-gspread-wks-update-cel'''
    #Find the cell containing next wednesdays date
    #cell = ws_results.find(next_wednesday) 
    #row = cell.row
    #col = colnum_string(cell.col) #Convert col number to letter
    #range = str(col)+str(row) #Put col letter with row number
    #values = [values, []] #Update func expecting list of lists
    #ws_results.update(range, 
    #                  values, 
    #                  major_dimension='ROWS', 
    #                  value_input_option='USER_ENTERED')
    values.append((next_wednesday)) #Add date to values
    sql = ''' UPDATE results
              SET	"Date" = ? ,
	                "Team A Result?" = ? ,
	                "Team B Result?" = ? ,
	                "Team A Total" = ? ,
	                "Team B Total" = ? ,
	                "Team A Player 1" = ? ,
	                "Team A Player 2" = ? ,
	                "Team A Player 3" = ? ,
	                "Team A Player 4" = ? ,
	                "Team A Player 5" = ? ,
	                "Team B Player 1" = ? ,
	                "Team B Player 2" = ? ,
	                "Team B Player 3" = ? ,
	                "Team B Player 4" = ? ,
	                "Team B Player 5" = ? ,
	                "Team A Colour" = ? ,
	                "Team B Colour" = ?
              WHERE "Date" = ?;'''
    c = conn.cursor()
    c.execute(sql, values)
    conn.commit()
    #Wipe tally once teams posted to the results page
    wipe_tally()
    return

def update_tally(values):
    '''Function to update the player 
    tally using the values from the index page
    Takes in values to be added as a list 
    to sheet and returns the gspread command 
    for updating the cell'''
    #col = ws_players.find('Playing')
    #col = colnum_string(col.col) #Convert col number to letter
    #range = str(col)+'2'
    #values = [values, []] #Update func expecting list of lists
    # sql = ''' UPDATE players 
    #           SET "Playing" = ?;'''
    # cur = conn.cursor()
    # cur.executemany(sql, ((val,) for val in values))
    # conn.commit()
    # print("Updated Tally")
    c = conn.cursor()
    for name in values:
        c.execute(f'UPDATE players SET Playing = "x" WHERE Name = "{name}"')
    conn.commit()
    #return ws_players.update(range, values, major_dimension='COLUMNS')
    return

def append_result(values):
    '''Function to update the result 
    using the values from the results page
    Takes in values to be added to sheet 
    and returns the gspread command for 
    appending the row'''
    #ws_results.append_row(values, 
    #                      value_input_option='USER_ENTERED')
    sql = ''' INSERT INTO results (
                            "Date",
                            "Team A Result?",
                            "Team B Result?",
	                        "Team A Total",
	                        "Team B Total",
	                        "Team A Player 1",
	                        "Team A Player 2",
	                        "Team A Player 3",
	                        "Team A Player 4",
	                        "Team A Player 5",
	                        "Team B Player 1",
	                        "Team B Player 2",
	                        "Team B Player 3",
	                        "Team B Player 4",
	                        "Team B Player 5",
	                        "Team A Colour",
	                        "Team B Colour")
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
    c = conn.cursor()
    c.execute(sql, values)
    conn.commit()
    return wipe_tally() #Wipe tally once teams posted to the results page

def update_score_result(values):
    '''Function to update the result using 
    the values from the results page
    Takes in values to be added to sheet and 
    returns the gspread command for updating row
    Updates both Score A and Score B 
    from a list of two values.'''
    #row = ws_results.find('-')
    #row = row.row
    #col = ws_results.find('Team A Result?')
    #col = colnum_string(col.col) #Convert col number to letter
    #range = str(col)+str(row) #Put col letter with row number
    #values = [values, []] #Update func expecting list of lists
    values.append((next_wednesday)) #Add date to values
    sql = ''' UPDATE results
              SET   "Team A Result?" = ? ,
	                "Team B Result?" = ?
              WHERE "Date" = ? AND "Team A Result?" = "-"; '''
    c = conn.cursor()
    c.execute(sql, values)
    conn.commit()
    #return ws_results.update(range, values, major_dimension='ROWS')
    update_all_formulas()
    return

def update_scorea(value):
    '''Function to update the result using 
    the values from the results page
    Takes in value to be added to sheet and 
    returns the gspread command for updating cell'''
    #row = ws_results.find('-')
    #col = ws_results.find('Team A Result?')
    #return ws_results.update_cell(row.row, col.col, value)
    #value.append((next_wednesday)) #Add date to values
    sql = f''' UPDATE results
              SET   "Team A Result?" = {value}
              WHERE "Date" = "{next_wednesday}" AND "Team A Result?" = "-"; '''
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    update_all_formulas()
    return

def update_scoreb(value):
    '''Function to update the result using 
    the values from the results page
    Takes in value to be added to sheet and 
    returns the gspread command for updating cell'''
    #row = ws_results.find('-')
    #col = ws_results.find('Team B Result?')
    #return ws_results.update_cell(row.row, col.col, value)
    #value = [value, next_wednesday] #Add date to values
    sql = ''' UPDATE results
              SET   "Team B Result?" = ?
              WHERE "Date" = ? AND "Team B Result?" = "-"; '''
    c = conn.cursor()
    c.execute(sql, (value, next_wednesday))
    conn.commit()
    update_all_formulas()
    return

def update_coloura(value):
    '''Function to update the colour using 
    the values from the results page
    Takes in value to be added to sheet and 
    returns the gspread command for updating cell'''
    #row = ws_results.find('-')
    #col = ws_results.find('Team A Colour')
    #return ws_results.update_cell(row.row, col.col, value)
    value = [value, next_wednesday] #Add date to values
    sql = ''' UPDATE results
              SET   "Team A Colour" = ?
              WHERE "Date" = ? AND "Team A Result?" = "-"; '''
    c = conn.cursor()
    c.execute(sql, value)
    conn.commit()

def update_colourb(value):
    '''Function to update the colour using 
    the values from the results page
    Takes in value to be added to sheet and 
    returns the gspread command for updating cell'''
    #row = ws_results.find('-')
    #col = ws_results.find('Team B Colour')
    #return ws_results.update_cell(row.row, col.col, value)
    value = [value, next_wednesday] #Add date to values
    sql = ''' UPDATE results
              SET   "Team B Colour" = ?
              WHERE "Date" = ? AND "Team A Result?" = "-"; '''
    c = conn.cursor()
    c.execute(sql, value)
    conn.commit()

def update_playing_status(player):
    '''Takes in a player 
    and adds x into the playing column'''
    #cell_name = ws_players.find(player) #Find the Players name and the row
    #clm_playing = ws_players.find('Playing') #Find the Playing column
    #ws_players.update_cell(cell_name.row, clm_playing.col, 'x')
    player = [player, next_wednesday] #Add date to values
    sql = ''' UPDATE players
              SET   "Playing" = "x"?
              WHERE "Name" = ?; '''
    c = conn.cursor()
    c.execute(sql, player)
    conn.commit()
    print("Updated playing status for:",player)
    return

def swap_player(players):
    '''Takes in a list of two players
    finds their score and swaps them 
    in the results table'''

    # result = results()
    # df = result.all_results()
    # last_row = df.loc[df['Date'] == next_wednesday]
    # result = df.loc[df['Team A Player 1'].str.contains(pat = 'Bernard')]
    # print(result)

    c = conn.cursor()
    #Find the Current Players name and the row
    #player_current = ws_players.find(player[0])
    player_current = players[0]

    #Find the New Players name and the row
    #player_new = ws_players.find(player[1]) 
    player_new = players[1]

    #Find the Total column
    #clm_total = ws_players.find('Total')

    #Convert Total Col Number to a Letter
    #clm_total = colnum_string(clm_total.col) 

    #Combine Col letter and row num into range
    #player_current_range = str(clm_total)+str(player_current.row)

    #Combine Col letter and row num into range
    #player_new_range = str(clm_total)+str(player_new.row) 

    #Grab score cell using range
    #player_current_score = ws_players.acell(player_current_range).value 
    player_current_score = c.execute(
        'SELECT "Total" FROM players WHERE "Name" = ?;', (players[0], ))
    player_current_score = c.fetchone()
    player_current_score = player_current_score[0]
    #Grab score cell using range
    #player_new_score = ws_players.acell(player_new_range).value 
    player_new_score = c.execute(
        'SELECT "Total" FROM players WHERE "Name" = ?;', (players[1], ))
    player_new_score = c.fetchone()
    player_new_score = player_new_score[0]
    #Work out difference between player scores
    player_score_difference = int(player_current_score) \
                                  - int(player_new_score)

    # print(f"The difference between player \
    #     scores is {player_score_difference}")
    #row = ws_results.find('-') #Find the row with dash

    #Find the Current Players name on the row with a dash
    #player_current = ws_results.find(player[0], in_row=row.row) 

    #If player col number > 10 E.g. above J then team is B  
    # if player_current.col > 10 : 
    #     team = "B"
    # else:
    #     team = "A"
    result = results()
    teamb = result.teamb()
    if player_current in teamb : 
        team = "B"
    else:
        team = "A"
    #Find the column with the score from Team A or B
    #col_result_num = ws_results.find('Team ' + team + ' Total')
    #col_result_num = f'"Team " + {team} + " Total"'
    col_result_num = f'Team {team} Total'
    col_player1 = f'Team {team} Player 1'
    col_player2 = f'Team {team} Player 2'
    col_player3 = f'Team {team} Player 3'
    col_player4 = f'Team {team} Player 4'
    col_player5 = f'Team {team} Player 5'

    #Convert Col Number to a Letter
    #col_result = colnum_string(col_result_num.col) 

    #Combine Col letter and row num into range
    #team_result_range = str(col_result)+str(row.row) 

    #Grab current score for Team A or B
    #team_result = ws_results.acell(team_result_range).value

    team_result = c.execute(
        f'SELECT "{col_result_num}" FROM results WHERE "Date" = "{next_wednesday}"')
    team_result = c.fetchone()
    team_result = team_result[0]
    #New Result is current result minus difference
    new_result = int(team_result) - player_score_difference 

    ##Update cell with new score,
    ##using the row with the dash,
    ##and column with Team Result
    #ws_results.update_cell(row.row, col_result_num.col, new_result)
    c.execute(f'UPDATE results SET "{col_result_num}" = {new_result} WHERE "Date" = "{next_wednesday}"')

    ##Update cell with new player,
    ##using the row with the dash,
    ##and column with Player Current
    #ws_results.update_cell(row.row, player_current.col, player[1])
    c.execute(f'UPDATE results SET "{col_player1}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{col_player1}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{col_player2}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{col_player2}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{col_player3}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{col_player3}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{col_player4}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{col_player4}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{col_player5}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{col_player5}" = "{player_current}"')

    print("Swapped player and updated score")
    return

def swap_existing_player(players):
    '''Takes in a list of two players
    finds their score and swaps them 
    in the results table if players
    are both playing'''

    c = conn.cursor()
    #Find the Current Players name and the row
    #player_current = ws_players.find(player[0])
    player_current = players[0]

    #Find the New Players name and the row
    #player_new = ws_players.find(player[1])
    player_new = players[1]

    #Find the Total column
    #clm_total = ws_players.find('Total')

    #Convert Total Col Number to a Letter
    #clm_total = colnum_string(clm_total.col) 

    #Combine Col letter and row num into range
    #player_current_range = str(clm_total)+str(player_current.row)

    #Combine Col letter and row num into range
    #player_new_range = str(clm_total)+str(player_new.row) 

    #Grab score cell using range
    #player_current_score = ws_players.acell(player_current_range).value 

    #Grab score cell using range
    #player_new_score = ws_players.acell(player_new_range).value 

    #Work out difference between player scores
    #player_score_difference = int(player_current_score) \
    #                              - int(player_new_score)

    #print(f"The difference between player \
    #    scores is {player_score_difference}")
    #row = ws_results.find('-') #Find the row with dash

    # #Find the Current Players name on the row with a dash
    # player_current = ws_results.find(player[0], in_row=row.row) 

    # #Find the New Players name on the row with a dash
    # player_new = ws_results.find(player[1], in_row=row.row) 

    #Grab score cell using range
    #player_current_score = ws_players.acell(player_current_range).value 
    player_current_score = c.execute(
        'SELECT "Total" FROM players WHERE "Name" = ?;', (players[0], ))
    player_current_score = c.fetchone()
    player_current_score = player_current_score[0]
    #Grab score cell using range
    #player_new_score = ws_players.acell(player_new_range).value 
    player_new_score = c.execute(
        'SELECT "Total" FROM players WHERE "Name" = ?;', (players[1], ))
    player_new_score = c.fetchone()
    player_new_score = player_new_score[0]
    #Work out difference between player scores
    player_score_difference = int(player_current_score) \
                                  - int(player_new_score)

    # #If player col number > 10 E.g. above J then team is B  
    # if player_current.col > 10 : 
    #     team_curr = "B"
    #     team_new = "A"
    # else:
    #     team_curr = "A"
    #     team_new = "B"

    result = results()
    teamb = result.teamb()
    if player_current in teamb : 
        team_curr = "B"
        team_new = "A"
    else:
        team_curr = "A"
        team_new = "B"

    curr_player1 = f'Team {team_curr} Player 1'
    curr_player2 = f'Team {team_curr} Player 2'
    curr_player3 = f'Team {team_curr} Player 3'
    curr_player4 = f'Team {team_curr} Player 4'
    curr_player5 = f'Team {team_curr} Player 5'
    new_player1 = f'Team {team_new} Player 1'
    new_player2 = f'Team {team_new} Player 2'
    new_player3 = f'Team {team_new} Player 3'
    new_player4 = f'Team {team_new} Player 4'
    new_player5 = f'Team {team_new} Player 5'

    # #Find the column with the score from Team A or B
    # col_result_num_a = ws_results.find('Team ' + team_curr + ' Total')

    # #Find the column with the score from Team A or B
    # col_result_num_b = ws_results.find('Team ' + team_new + ' Total') 

    # #Convert Col Number to a Letter
    # col_result_a = colnum_string(col_result_num_a.col)

    # #Convert Col Number to a Letter
    # col_result_b = colnum_string(col_result_num_b.col)

    # #Combine Col letter and row num into range
    # team_result_range_a = str(col_result_a)+str(row.row)

    # #Combine Col letter and row num into range
    # team_result_range_b = str(col_result_b)+str(row.row)

    # #Grab current score for Team A
    # team_result_a = ws_results.acell(team_result_range_a).value
    team_result_a = c.execute(
        f'SELECT "Team A Total" FROM results WHERE "Date" = "{next_wednesday}"')
    team_result_a = c.fetchone()
    team_result_a = team_result_a[0]

    # #Grab current score for Team B
    # team_result_b = ws_results.acell(team_result_range_b).value
    team_result_b = c.execute(
        f'SELECT "Team B Total" FROM results WHERE "Date" = "{next_wednesday}"')
    team_result_b = c.fetchone()
    team_result_b = team_result_b[0]

    # #New Result is current result minus difference
    new_result_a = int(team_result_a) - player_score_difference

    # #New Result is current result minus difference
    new_result_b = int(team_result_b) - player_score_difference

    # ##Update cell with new score,
    # ##using the row with the dash,
    # ##and column with Team Result
    # ws_results.update_cell(row.row, col_result_num_a.col, new_result_a)
    # ws_results.update_cell(row.row, col_result_num_b.col, new_result_b)
    c.execute(f'UPDATE results SET "Team A Total" = {new_result_a} WHERE "Date" = "{next_wednesday}"')
    c.execute(f'UPDATE results SET "Team B Total" = {new_result_b} WHERE "Date" = "{next_wednesday}"')

    # ##Update cell with new player,
    # ##using the row with the dash,
    # ##and column with Player Current/New
    # ws_results.update_cell(row.row, player_current.col, player[1])
    # ws_results.update_cell(row.row, player_new.col, player[0])
    c.execute(f'UPDATE results SET "{curr_player1}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{curr_player1}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{curr_player2}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{curr_player2}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{curr_player3}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{curr_player3}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{curr_player4}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{curr_player4}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{curr_player5}" = "{player_new}" WHERE "Date" = "{next_wednesday}" AND "{curr_player5}" = "{player_current}"')
    c.execute(f'UPDATE results SET "{new_player1}" = "{player_current}" WHERE "Date" = "{next_wednesday}" AND "{new_player1}" = "{player_new}"')
    c.execute(f'UPDATE results SET "{new_player2}" = "{player_current}" WHERE "Date" = "{next_wednesday}" AND "{new_player2}" = "{player_new}"')
    c.execute(f'UPDATE results SET "{new_player3}" = "{player_current}" WHERE "Date" = "{next_wednesday}" AND "{new_player3}" = "{player_new}"')
    c.execute(f'UPDATE results SET "{new_player4}" = "{player_current}" WHERE "Date" = "{next_wednesday}" AND "{new_player4}" = "{player_new}"')
    c.execute(f'UPDATE results SET "{new_player5}" = "{player_current}" WHERE "Date" = "{next_wednesday}" AND "{new_player5}" = "{player_new}"')
    print("Swapped player and updated score")
    return


def modify_playing_status(player):
    '''Takes in a player
    and adds o into the playing column'''

    #Find the Players name and the row
    #cell_name = ws_players.find(player) 

    #Find the Playing column
    #clm_playing = ws_players.find('Playing') 

    #ws_players.update_cell(cell_name.row, 
    #                       clm_playing.col, 
    #                       'o')
    sql = f'''   UPDATE players 
                SET "Playing" = "o"
                WHERE "Name" = "{player}"; '''
    c = conn.cursor()
    c.execute(sql, player)
    conn.commit()
    print("Modified playing status for:",player)
    return

def add_new_player(player):
    '''Appends New Row with a new 
    player and generic score'''

    #Add generic score to playername
    new_player = [player,int(77)] 

    #Should be a list of name and score
    #ws_players.append_row(new_player) 
    sql = ''' INSERT INTO players (
                            "Name",
                            "Total")
              VALUES (?,?);'''
    c = conn.cursor()
    c.execute(sql, new_player)
    conn.commit()
    print("Appended new row for:",new_player)
    #Run the copy formulas func using first element of list as name
    #return copy_formulas(new_player[0])
    update_all_formulas()
    return

def remove_player(player):
    '''Appends New Row with a new 
    player and generic score
    Expects two items in a list, Name and Score'''
    #cell_name = ws_players.find(player)
    #ws_players.delete_row(cell_name.row)
    sql = f''' DELETE FROM players
              WHERE "Name" = "{player}";'''
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    print("Deleted row for:",player)
    return

def update_wins():
    '''Updates formulas for wins'''
    players = player()
    player_names = players.all_players()
    c = conn.cursor()
    for name,total in player_names:
        print(f"Sending {name} for Win calculation.")
        calc = calc_wins(name)
        c.execute(f'UPDATE players SET Wins = {calc} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Wins")
    return

def update_draws():
    '''Updates formulas for draws'''
    players = player()
    player_names = players.all_players()
    c = conn.cursor()
    for name,total in player_names:
        calc = calc_draws(name)
        c.execute(f'UPDATE players SET Draws = {calc} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Draws")
    return

def update_losses():
    '''Updates formulas for losses'''
    players = player()
    player_names = players.all_players()
    c = conn.cursor()
    for name,total in player_names:
        calc = calc_losses(name)
        c.execute(f'UPDATE players SET Losses = {calc} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Losses")
    return

def update_score():
    '''Updates formulas for score'''
    players = player()
    player_names = players.all_players()
    c = conn.cursor()
    for name,total in player_names:
        calc = calc_score(name)
        c.execute(f'UPDATE players SET Score = {calc} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Score")
    return

def update_played():
    '''Updates formulas for Played'''
    players = player()
    player_names = players.all_players()
    c = conn.cursor()
    for name,total in player_names:
        calc = calc_played(name)
        c.execute(f'UPDATE players SET Played = {calc} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Played")
    return

def update_percent():
    '''Updates formulas for Percent Calc'''
    players = player()
    player_names = players.all_players()
    c = conn.cursor()
    for name,total in player_names:
        calc = calc_percent(name)
        c.execute(f'UPDATE players SET "Percent Calc" = {calc} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Percent Calc")
    return

def update_wpercent():
    '''Updates formulas for Win Percentage'''
    players = player()
    player_names = players.all_players()
    c = conn.cursor()
    for name,total in player_names:
        calc = calc_wpercent(name)
        c.execute(f'UPDATE players SET "Win Percentage" = {calc} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Win Percentage")
    return

def update_player_totals(totals):
    '''Updates player totals from html'''
    c = conn.cursor()
    for name,total in totals:
        c.execute(f'UPDATE players SET "Total" = {total} WHERE Name = "{name}"')
    conn.commit()
    print("Updated Player Totals")
    return

def update_player_names(player):
    '''Updates player names from html'''
    c = conn.cursor()
    for oldname,newname in player:
        c.execute(f'UPDATE players SET "Name" = "{newname}" WHERE Name = "{oldname}"')
    conn.commit()
    print("Updated Player Names")
    return

def update_all_formulas():
    '''Updates all formulas'''
    update_wins()
    update_draws()
    update_losses()
    update_score()
    update_played()
    #update_percent() #Guilio has a NONE result which breaks the update
    update_wpercent()
    return

def calc_wins(player):
    '''Calculate wins for each player
    Where player is on the team and result 
    is < OR > opposite result'''
    sql = f'''SELECT 
        COUNT(CASE WHEN "Team A Player 1" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 2" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 3" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 4" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 5" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 1" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 2" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 3" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 4" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 5" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END)
            FROM results;'''
    c = conn.cursor()
    result = c.execute(sql)
    result = c.fetchone()
    result = result[0]
    print(f'Calulated {player}s wins as {result}')
    return result

def calc_draws(player):
    '''Calculate wins for each player
    Where player is on the team and result 
    is equal to opposite result'''
    sql = f'''SELECT 
        COUNT(CASE WHEN "Team A Player 1" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 2" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 3" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 4" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 5" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 1" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 2" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 3" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 4" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 5" = "{player}" AND "Team A Result?" = "Team B Result?" THEN 1 END)
            FROM results;'''
    c = conn.cursor()
    result = c.execute(sql)
    result = c.fetchone()
    result = result[0]
    print(f'Calulated {player}s draws as {result}')
    return result

def calc_losses(player):
    '''Calculate wins for each player
    Where player is on the team and result 
    is < OR > opposite result'''
    sql = f'''SELECT 
        COUNT(CASE WHEN "Team A Player 1" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 2" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 3" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 4" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team A Player 5" = "{player}" AND "Team A Result?" < "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 1" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 2" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 3" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 4" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END) +
        COUNT(CASE WHEN "Team B Player 5" = "{player}" AND "Team A Result?" > "Team B Result?" THEN 1 END)
            FROM results;'''
    c = conn.cursor()
    result = c.execute(sql)
    result = c.fetchone()
    result = result[0]
    print(f'Calulated {player}s losses as {result}')
    return result

def calc_score(player):
    '''Calculate score by Adding Wins to Draws'''
    sql = f'''SELECT (Wins * 3 + Draws) 
            FROM players
            WHERE Name = "{player}";'''
    c = conn.cursor()
    result = c.execute(sql)
    result = c.fetchone()
    result = result[0]
    print(f'Calulated {player}s score as {result}')
    return result

def calc_played(player):
    '''Calculate Played by Adding Wins to Draws to Losses'''
    sql = f'''SELECT (Wins + Draws + Losses) 
            FROM players
            WHERE Name = "{player}";'''
    c = conn.cursor()
    result = c.execute(sql)
    result = c.fetchone()
    result = result[0]
    print(f'Calulated {player}s games played as {result}')
    return result

def calc_percent(player):
    '''Calculate Percentage Calc'''
    sql = f'''SELECT (Wins / Played * 100) 
            FROM players
            WHERE Name = "{player}";'''
    c = conn.cursor()
    result = c.execute(sql)
    result = c.fetchone()
    result = result[0]
    print(f'Calulated {player}s percent calc as {result}')
    return result

def calc_wpercent(player):
    '''Calculate Win Percentage'''
    sql = f'''SELECT 
        CASE WHEN Wins < 5 THEN 0 ELSE (Wins / Played * 100) END
            FROM players
            WHERE Name = "{player}";'''
    c = conn.cursor()
    result = c.execute(sql)
    result = c.fetchone()
    result = result[0]
    print(f'Calulated {player}s win percentage as {result}')
    return result #All results seem to be zero