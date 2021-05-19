from flask import render_template, request, Blueprint
from services.json_date import next_wednesday
from services.getplayers import SERVICE, SPREADSHEET_ID, WRITE_RANGE_NAME

result_blueprint = Blueprint('result', __name__, template_folder='templates', static_folder='static')

@result_blueprint.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Use GetList to put the data from the index template into the array
        teama_passback = []
        teama_passback = request.form.getlist('teama_passback')
        teamb_passback = []
        teamb_passback = request.form.getlist('teamb_passback')
        scorea_passback = []
        scorea_passback = request.form.getlist('scorea_passback')
        scoreb_passback = []
        scoreb_passback = request.form.getlist('scoreb_passback')
        # Post Results to Google Sheets if output is checked
        output_checked = []
        output_checked = request.form.getlist('output_checked')
        if output_checked == ['Yes']:
            # Format the google ouput into one long comma sep str
            google_output = []
            google_output.append((next_wednesday))
            google_output.append((0))
            google_output.append((0))
            google_output.append((scorea_passback))
            google_output.append((scoreb_passback))
            for obj in teama_passback: 
                google_output.append((obj))
            for obj in teamb_passback: 
                google_output.append((obj))
            # Format the google body for ROWS
            body = {
                'majorDimension': 'ROWS',
                'values': [
                    google_output,
                ],
                }
            # Print the result to google sheets with append enabled
            result = SERVICE.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID, range=WRITE_RANGE_NAME,
                valueInputOption='USER_ENTERED', body=body).execute()
        # Return Team A and Team B to the results template
        return render_template('post.html')
    # If request method is not POST then it must be GET
    return render_template('result.html')