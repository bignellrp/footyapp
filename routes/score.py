from flask import render_template, request, Blueprint
from services.getplayers import _fetch_stats_sheet, _make_score, SPREADSHEET_ID, sheet

score_blueprint = Blueprint('score', __name__, template_folder='templates', static_folder='static')

@score_blueprint.route('/score', methods=['GET', 'POST'])
def score():
    make_score, end_row = _make_score(_fetch_stats_sheet())
    this_weeks_teams = []
    for obj in make_score:
        this_weeks_teams.append((obj.date , obj.teama_1 , obj.teama_2, obj.teama_3 , obj.teama_4, obj.teama_5 , obj.teamb_1, obj.teamb_2, obj.teamb_3 , obj.teamb_4, obj.teamb_5))
    team_var = this_weeks_teams[-1]
    date = team_var[0]
    str(date)
    date = date[1:-1]
    teama = team_var[1],team_var[2],team_var[3],team_var[4],team_var[5]
    teamb = team_var[6],team_var[7],team_var[8],team_var[9],team_var[10]
    if request.method == 'POST':
        score_input_a = []
        score_input_a = request.form.get('score_input_a')
        score_input_b = []
        score_input_b = request.form.get('score_input_b')
        score_output = []
        score_output.append((score_input_a))
        score_output.append((score_input_b))
        # Grab game score from google sheets and display them in a score table
        ##Format the google body for ROWS
        body = {
            'majorDimension': 'ROWS',
            'values': [
                score_output
            ],
            }
        #end_row = "10"
        end_row = end_row + 1
        range_ = 'Results!B'+str(end_row)
        ##Print the result to google sheets with update enabled
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_,
            valueInputOption='USER_ENTERED', body=body).execute()
        return render_template('post.html')
    ##If request method is not POST then it must be GET
    return render_template('score.html', teama = teama, teamb = teamb, date = date)