import gspread
from numpy.lib.stride_tricks import broadcast_arrays
from services.get_date import next_wednesday

#GSPREAD Vars
SERVICE_ACCOUNT_FILE = './services/keys.json'
SPREADSHEET_ID = '1tyy_8sKM-N-JA6j1pASCO6_HRxvlhTuA3R0KysbVG9U'
PLAYERS_WORKSHEET = 'Dev Players'
RESULTS_WORKSHEET = 'Dev Results'

#GSPREAD Objects
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
ss = gc.open_by_key(SPREADSHEET_ID)
wsp = ss.worksheet(PLAYERS_WORKSHEET)
wsr = ss.worksheet(RESULTS_WORKSHEET) 

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

def _update_result(values):
    '''Function to update the result row using the values from the results page
    Takes in values to be added to sheet and returns the gspread command for updating row'''
    cell = wsr.find(next_wednesday) #Find the cell containing next wednesdays date
    row = cell.row
    col = cell.col
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+str(row) #Put col letter with row number
    values = [values, []] #Update func expecting list of lists
    return wsr.update(range, values, major_dimension='ROWS')

def _update_tally(values):
    '''Function to update the player tally using the values from the index page
    Takes in values to be added as a list to sheet and returns the gspread command for updating the cell'''
    col = wsp.find('Playing')
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+'2'
    values = [values, []] #Update func expecting list of lists
    #return wsp.update('G2', body, raw=False, major_dimension='COLUMNS')
    return wsp.update(range, values, major_dimension='COLUMNS')

def _append_result(values):
    '''Function to update the result using the values from the results page
    Takes in values to be added to sheet and returns the gspread command for appending the row'''
    print(values) #Seems to have an extra ' on the date??
    return wsr.append_row(values)

def _update_score_result(values):
    '''Function to update the result using the values from the results page
    Takes in values to be added to sheet and returns the gspread command for updating row'''
    row = wsr.find(next_wednesday)
    row = row.row
    col = wsr.find('Team A Result?')
    col = colnum_string(col.col) #Convert col number to letter
    range = str(col)+str(row) #Put col letter with row number
    values = [values, []] #Update func expecting list of lists
    return wsr.update(range, values, major_dimension='ROWS')