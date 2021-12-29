import os
from flask import Flask, session, redirect, url_for
from services.lookup import lookup
from routes import *
import bot #Used even though shows as not accessed
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from services.lookup import lookup
from services.get_oscommand import GITBRANCH, IFBRANCH

if IFBRANCH in GITBRANCH:
    OAUTH2_CLIENT_ID = lookup("discord_client_id")
    OAUTH2_CLIENT_SECRET = lookup("discord_client_secret")
else:
    OAUTH2_CLIENT_ID = lookup("discord_client_id_dev")
    OAUTH2_CLIENT_SECRET = lookup("discord_client_secret_dev")

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

def welcome_user(user):
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )

@app.route("/login/")
def login():
    return discord.create_session()

@app.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    welcome_user(user)
    return redirect(url_for("index.index"))

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""

##Register the blueprint for each route
app.register_blueprint(index_blueprint)
app.register_blueprint(compare_blueprint)
app.register_blueprint(leaderboard_blueprint)
app.register_blueprint(stats_blueprint)
app.register_blueprint(result_blueprint)
app.register_blueprint(score_blueprint)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)