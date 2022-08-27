from routes import *

def create_app():
    
    from flask import Flask
    app = Flask(__name__)

    ##Register the blueprint for each route
    app.register_blueprint(index_blueprint)
    app.register_blueprint(compare_blueprint)
    app.register_blueprint(leaderboard_blueprint)
    app.register_blueprint(stats_blueprint)
    app.register_blueprint(result_blueprint)
    app.register_blueprint(score_blueprint)
    app.register_blueprint(playertotals_blueprint)

    return app