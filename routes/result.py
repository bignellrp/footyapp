from flask import render_template, request, Blueprint
from services.get_date import next_wednesday
from services.store_results import _update_result, _append_result
from services.get_players import _get_results_table, _fetch_results_table

result_blueprint = Blueprint('result', __name__, template_folder='templates', static_folder='static')

@result_blueprint.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        ##Use GetList to put the data from the index template into the array
        teama_passback = request.form.getlist('teama_passback')
        teamb_passback = request.form.getlist('teamb_passback')
        scorea_passback = request.form.get('scorea_passback')
        scoreb_passback = request.form.get('scoreb_passback')
        ##Bringing back results from html was found to cause issues with lists
        ##Using replace and split to reform the lists
        teama_passback = teama_passback[0].replace(',','').replace("'",'').replace('{','').replace('}','').replace('[','').replace(']','').split()
        teamb_passback = teamb_passback[0].replace(',','').replace("'",'').replace('{','').replace('}','').replace('[','').replace(']','').split()
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
        ## If the last row has next wednesdays date then replace the results
        ## Else append results on a new line
        _,_,_,dash,date,_ = _get_results_table(_fetch_results_table())
        if date == next_wednesday and dash == "-":
            result = _update_result(body)
            print("Running update function")
        else:
            result = _append_result(body)
            print("Running append function")
        ##Return Team A and Team B to the results template
        return render_template('post.html')
    ##If request method is not POST then it must be GET
    return render_template('result.html')