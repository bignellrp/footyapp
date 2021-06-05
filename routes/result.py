from flask import render_template, request, Blueprint, session
from services.get_date import next_wednesday
from services.store_results import _update_result, _append_result
from services.get_players import _get_results_table, _fetch_results_table

result_blueprint = Blueprint('result', __name__, template_folder='templates', static_folder='static')

@result_blueprint.route('/result', methods=['GET', 'POST'])
def result():
    '''A function for building the results page.
    Takes in teama and teamb from flask session so result carries between pages
    and returns the body to the google sheet in row format'''
    
    if request.method == 'POST':

        ##Pull data from flask session
        ##Taken from reddit https://www.reddit.com/r/flask/comments/nsghsf/hidden_list/
        teama_passback = session['team_a']
        teamb_passback = session['team_b']
        scorea_passback = session['team_a_total']
        scoreb_passback = session['team_b_total']

        ##Build google_output list of values in a row
        google_output = []
        google_output.append((next_wednesday))
        google_output.append(str("-"))
        google_output.append(str("-"))
        google_output.append((scorea_passback))
        google_output.append((scoreb_passback))
        google_output.extend((teama_passback))
        google_output.extend((teamb_passback))

        ##Format the google body for ROWS
        body = {
            'majorDimension': 'ROWS',
            'values': [
                google_output,
            ],
            }

        _,_,_,dash,date,_ = _get_results_table(_fetch_results_table())

        if date == next_wednesday and dash == "-":
            '''If the last row has next wednesdays date 
            then replace the results.
            Else append results on a new line'''
            result = _update_result(body)
            print("Running update function")
        else:
            result = _append_result(body)
            print("Running append function")

        ##Return Team A and Team B to the results template
        return render_template('post.html')

    ##If request method is not POST then it must be GET
    return render_template('result.html')