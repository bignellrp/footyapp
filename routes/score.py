from flask import render_template, request, Blueprint
from services.getplayers import stats_table, _make_score
from services.getplayers import sheet, SPREADSHEET_ID, STATS_TABLE_WRITE
from operator import itemgetter

score_blueprint = Blueprint('score', __name__, template_folder='templates', static_folder='static')

@score_blueprint.route('/score', methods=['GET', 'POST'])
def score():
    make_score = _make_score(stats_table)
    this_weeks_teams = []
    for obj in make_score:
        this_weeks_teams.append((obj.date , obj.teama_1 , obj.teama_2, obj.teama_3 , obj.teama_4, obj.teama_5 , obj.teamb_1, obj.teamb_2, obj.teamb_3 , obj.teamb_4, obj.teamb_5))

    team_var = this_weeks_teams[-1]
    date = team_var[0]
    str(date)
    date = date[1:-1]
    teama = team_var[1],team_var[2],team_var[3],team_var[4],team_var[5]
    teamb = team_var[6],team_var[7],team_var[8],team_var[9],team_var[10]
    print(date)
    print(teama)
    print(teamb)

    if request.method == 'POST':
        
        score_input_a = []
        score_input_a = request.form.get('score_input_a')
        score_input_b = []
        score_input_b = request.form.get('score_input_b')
        
        print(score_input_a)
        print(score_input_b)
        # Grab game score from google sheets and display them in a score table
        ##Format the google body for ROWS
        body = {
            'majorDimension': 'ROWS',
            'values': [
                score_input_a,score_input_b
            ],
            }
        row = "10"
        range_ = 'B'+str(row)
        #Print the result to google sheets with update enabled
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_,
            valueInputOption='USER_ENTERED', body=body).execute()

        return render_template('post.html')
    ##If request method is not POST then it must be GET
    return render_template('score.html', teama = teama, teamb = teamb, date = date)