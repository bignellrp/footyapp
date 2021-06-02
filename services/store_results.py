from services.getplayers import sheet, SPREADSHEET_ID, _make_score, _fetch_stats_sheet

## Function to get the end row from stats table to append to
## TODO Can i grab just end_row from getplayers (it will need the plus 1)
def _get_stats_endrow():
    make_score, end_row = _make_score(_fetch_stats_sheet())
    end_row = end_row + 1
    print(end_row)
    return end_row

def _get_stats():
    make_score, end_row = _make_score(_fetch_stats_sheet())
    this_weeks_teams = []
    for obj in make_score:
        this_weeks_teams.append((obj.date , obj.scorea, obj.teama_1 , obj.teama_2, obj.teama_3 , obj.teama_4, obj.teama_5 , obj.teamb_1, obj.teamb_2, obj.teamb_3 , obj.teamb_4, obj.teamb_5))
    team_var = this_weeks_teams[-1]
    date = team_var[0]
    #Dash is used in if statement. E.g. Only update if score is not already entered.
    dash = team_var[1]
    teama = team_var[2],team_var[3],team_var[4],team_var[5],team_var[6]
    teamb = team_var[7],team_var[8],team_var[9],team_var[10],team_var[11]
    return date,dash,teama,teamb

## Function to update the result using the UPDATE RANGE and the body from the results page
def _update_result(body):
    UPDATE_RANGE = 'Results!A'+str(_get_stats_endrow())
    print(UPDATE_RANGE)
    return sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()

## Function to append the result using the APPEND RANGE and the body from the results page
def _append_result(body):
    APPEND_RANGE = 'Results!A1:AA1000'
    print(APPEND_RANGE)
    return sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=APPEND_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()

## Function to update the result using the SCORE RANGE and the body from the results page
def _update_score_result(body):
    SCORE_RANGE = 'Results!B'+str(_get_stats_endrow())
    print(SCORE_RANGE)
    return sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=SCORE_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()