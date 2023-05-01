from flask import render_template, \
                request, Blueprint, session, redirect, url_for, send_file
from services.get_spread import player,results

download_blueprint = Blueprint('download', 
                            __name__, 
                            template_folder='templates', 
                            static_folder='static')

@download_blueprint.route('/download', methods=['GET'])

def download():

    '''Downloads the teams as txt'''

    result = results()
    teama = result.teama()
    teamb = result.teama()
    path = "/teama.csv"
    if request.method == 'GET':
        return send_file(path, as_attachment=True)