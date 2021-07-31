import gspread

SERVICE_ACCOUNT_FILE = './services/keys.json'
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'

gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
ss = gc.open_by_key(SPREADSHEET_ID)

def _update_playing_status_list(player_list):
    '''Takes in a list of players 
    and adds x into the playing column'''
    ws = ss.worksheet('Players') 
    for name in player_list:
        cell_name = ws.find(name) #Find the Players name and the row
        clm_playing = ws.find('Playing') #Find the Playing column
        ws.update_cell(cell_name.row, clm_playing.col, 'x')
        print("Updated playing status for:",name)
    return

def _update_playing_status(player):
    '''Takes in a player 
    and adds x into the playing column'''
    ws = ss.worksheet('Players') 
    cell_name = ws.find(player) #Find the Players name and the row
    clm_playing = ws.find('Playing') #Find the Playing column
    ws.update_cell(cell_name.row, clm_playing.col, 'x')
    print("Updated playing status for:",player)
    return

def _modify_playing_status_list(player_list):
    '''Takes in a list of players 
    and adds o into the playing column'''
    ws = ss.worksheet('Players') 
    for name in player_list:
        cell_name = ws.find(name) #Find the Players name and the row
        clm_playing = ws.find('Playing') #Find the Playing column
        ws.update_cell(cell_name.row, clm_playing.col, 'o')
        print("Modified playing status for:",name)
    return

def _modify_playing_status(player):
    '''Takes in a player
    and adds o into the playing column'''
    ws = ss.worksheet('Players') 
    cell_name = ws.find(player) #Find the Players name and the row
    clm_playing = ws.find('Playing') #Find the Playing column
    ws.update_cell(cell_name.row, clm_playing.col, 'o')
    print("Modified playing status for:",player)
    return

def _add_new_player(player):
    '''Appends New Row with a new 
    player and generic score'''
    ws = ss.worksheet('Players')
    new_player = [player,int(77)] #Add generic score to playername
    ws.append_row(new_player) #Should be a list of name and score
    print("Appended new row for:",new_player)
    return _copy_formulas(new_player[0]) #Run the copy formulas func using first element of list as name

def _remove_player(player):
    '''Appends New Row with a new 
    player and generic score
    Expects two items in a list, Name and Score'''
    ws = ss.worksheet('Players')
    cell_name = ws.find(player)
    ws.delete_row(cell_name.row)
    print("Deleted row for:",player)
    return

def _copy_formulas(player):
    '''Updates formulas for new players'''
    ws = ss.worksheet('Players')
    cell_name = ws.find(player)
    clm_wins = ws.find('Wins')
    clm_draws = ws.find('Draws')
    clm_losses = ws.find('Losses')
    clm_score = ws.find('Score')
    clm_playing = ws.find('Playing')
    #formula = ws.acell('G2', value_render_option='FORMULA').value
    wins_formula = '=SUM(SUMPRODUCT((Results!$F$2:$J$929 = $A{})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))+(SUMPRODUCT((Results!$K$2:$O$929 = $A{})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))'.format(cell_name.row,cell_name.row)
    draws_formula = '=SUM(SUMPRODUCT((Results!$F$2:$O$929 = $A{})*(Results!$B$2:$B$929=Results!$C$2:$C$929)))'.format(cell_name.row)
    losses_formula = '=SUM(SUMPRODUCT((Results!$F$2:$J$929 = $A{})*(Results!$B$2:$B$929<Results!$C$2:$C$929)))+(SUMPRODUCT((Results!$K$2:$O$929 = $A{})*(Results!$B$2:$B$929>Results!$C$2:$C$929)))'.format(cell_name.row,cell_name.row)
    score_formula = '=IFERROR((H{}*3+I{}),0)'.format(cell_name.row,cell_name.row)
    ws.update_cell(cell_name.row,clm_wins.col,wins_formula)
    ws.update_cell(cell_name.row,clm_draws.col,draws_formula)
    ws.update_cell(cell_name.row,clm_losses.col,losses_formula)
    ws.update_cell(cell_name.row,clm_score.col,score_formula)
    ws.update_cell(cell_name.row, clm_playing.col, 'x')
    print("Updated Formulas!")
    return