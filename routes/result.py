from flask import render_template, request, Blueprint
from services.json_date import next_wednesday
from services.getplayers import sheet, SPREADSHEET_ID, STATS_TABLE_WRITE

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
        google_output.append(str(0))
        google_output.append(str(0))
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
        ##Print the result to google sheets with append enabled
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID, range=STATS_TABLE_WRITE,
            valueInputOption='USER_ENTERED', body=body).execute()
        ##Return Team A and Team B to the results template
        return render_template('post.html')
    ##If request method is not POST then it must be GET
    return render_template('result.html')