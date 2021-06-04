from services.get_players import sheet, SPREADSHEET_ID, _get_results_table, _fetch_results_table

def _update_result(body):
    '''Function to update the result using the UPDATE RANGE and the body from the results page
    Takes in body of data to be added to sheet and returns the execute command for googleapi'''
    end_row,_,_,_,_,_ = _get_results_table(_fetch_results_table())
    UPDATE_RANGE = 'Results!A'+str(end_row)
    print(UPDATE_RANGE)
    return sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()

def _append_result(body):
    '''Function to append the result using the APPEND RANGE and the body from the results page
    Takes in body of data to be added to sheet and returns the execute command for googleapi'''
    APPEND_RANGE = 'Results!A1:AA1000'
    print(APPEND_RANGE)
    return sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=APPEND_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()

def _update_score_result(body):
    '''Function to update the result using the SCORE RANGE and the body from the results page
    Takes in body of data to be added to sheet and returns the execute command for googleapi'''
    end_row,_,_,_,_,_ = _get_results_table(_fetch_results_table())
    SCORE_RANGE = 'Results!B'+str(end_row)
    print(SCORE_RANGE)
    return sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=SCORE_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()