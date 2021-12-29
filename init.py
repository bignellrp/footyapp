from routes import *

def create_app():
    
    from flask import Flask
    from flask_discord import DiscordOAuth2Session
    from services.lookup import lookup
    from services.get_oscommand import GITBRANCH, IFBRANCH
    import os
    
    app = Flask(__name__)

    app.secret_key = lookup("session")
    # OAuth2 must make use of HTTPS in production environment.
    app.config["DISCORD_REDIRECT_URI"] = lookup("discord_redirect_uri")
    if 'http://' in app.config["DISCORD_REDIRECT_URI"]:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

    if  IFBRANCH in GITBRANCH:
        app.config["DISCORD_CLIENT_ID"] = lookup("discord_client_id")
        app.config["DISCORD_CLIENT_SECRET"] = lookup("discord_client_secret")
        app.config["DISCORD_BOT_TOKEN"] = lookup("discord_token")
    else:
        app.config["DISCORD_CLIENT_ID"] = lookup("discord_client_id_dev")
        app.config["DISCORD_CLIENT_SECRET"] = lookup("discord_client_secret_dev")
        app.config["DISCORD_BOT_TOKEN"] = lookup("discord_token_dev")

    discord = DiscordOAuth2Session(app)

    ##Register the blueprint for each route
    app.register_blueprint(index_blueprint)
    app.register_blueprint(compare_blueprint)
    app.register_blueprint(leaderboard_blueprint)
    app.register_blueprint(stats_blueprint)
    app.register_blueprint(result_blueprint)
    app.register_blueprint(score_blueprint)

    return app