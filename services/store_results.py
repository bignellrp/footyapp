from services.getplayers import sheet, SPREADSHEET_ID, _make_score, _fetch_stats_sheet

APPEND_RANGE = 'Results!A1:AA1000'

## Function to get the end row from stats table to append to
def _get_stats_endrow():
    make_score, end_row = _make_score(_fetch_stats_sheet())
    this_weeks_teams = []
    for obj in make_score:
        this_weeks_teams.append((obj.date))
    end_row = end_row + 1
    return end_row

## Use the endrow function for finding the end row for the update range variable
UPDATE_RANGE = 'Results!A'+str(_get_stats_endrow())

## Function to get the date from the end row to compare with
def _get_stats_date():
    make_score, end_row = _make_score(_fetch_stats_sheet())
    this_weeks_teams = []
    for obj in make_score:
        this_weeks_teams.append((obj.date))
    date = this_weeks_teams[-1]
    return date

## Function to update the result using the UPDATE RANGE and the body from the results page
def _update_result(body):
    return sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()

## Function to append the result using the APPEND RANGE and the body from the results page
def _append_result(body):
    return sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=APPEND_RANGE,
            valueInputOption='USER_ENTERED', body=body).execute()