#from flask import redirect, url_for
import bot #Used even though shows as not accessed
from init import create_app
from services.lookup import lookup
#from flask_discord import DiscordOAuth2Session, Unauthorized
from flask import Flask, render_template, request, redirect, session
from services.get_oscommand import GITBRANCH, IFBRANCH
#import os
#from zenora import APIClient
#from urllib.parse import quote

app = create_app()

app.secret_key = lookup("session")


# if IFBRANCH in GITBRANCH:
#     app.config["DISCORD_CLIENT_ID"] = lookup("discord_client_id")
#     app.config["DISCORD_CLIENT_SECRET"] = lookup("discord_client_secret")
#     app.config["DISCORD_BOT_TOKEN"] = lookup("discord_token")
#     app.config["DISCORD_REDIRECT_URI"] = lookup("discord_redirect_uri")
# else:
#     app.config["DISCORD_CLIENT_ID"] = lookup("discord_client_id_dev")
#     app.config["DISCORD_CLIENT_SECRET"] = lookup("discord_client_secret_dev")
#     app.config["DISCORD_BOT_TOKEN"] = lookup("discord_token_dev")
#     app.config["DISCORD_REDIRECT_URI"] = lookup("discord_redirect_uri_dev")

# if IFBRANCH in GITBRANCH:
#     DISCORD_CLIENT_ID = lookup("discord_client_id")
#     DISCORD_CLIENT_SECRET = lookup("discord_client_secret")
#     DISCORD_BOT_TOKEN = lookup("discord_token")
#     DISCORD_REDIRECT_URI = lookup("discord_redirect_uri")
# else:
#     DISCORD_CLIENT_ID = lookup("discord_client_id_dev")
#     DISCORD_CLIENT_SECRET = lookup("discord_client_secret_dev")
#     DISCORD_BOT_TOKEN = lookup("discord_token_dev")
#     DISCORD_REDIRECT_URI = lookup("discord_redirect_uri_dev")

# OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={quote(DISCORD_REDIRECT_URI)}&response_type=code&scope=identify"
# client = APIClient(DISCORD_BOT_TOKEN, client_secret=DISCORD_CLIENT_SECRET)

# @app.route("/login")
# def login():
#     return redirect(OAUTH_URL)


# @app.route("/logout")
# def logout():
#     session.pop("access_token")
#     return redirect("/")


# @app.route("/oauth/callback")
# def oauth_callback():
#     code = request.args["code"]
#     access_token = client.oauth.get_access_token(
#         code, redirect_uri=DISCORD_REDIRECT_URI
#     ).access_token
#     session["access_token"] = access_token

#     return redirect("/")

# # OAuth2 must make use of HTTPS in production environment.
# if 'http://' in app.config["DISCORD_REDIRECT_URI"]:
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

# discord = DiscordOAuth2Session(app)

# def welcome_user(user):
#     dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
#     return discord.bot_request(
#         f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
#     )

# @app.route("/login/")
# def login():
#     return discord.create_session()

# @app.route("/callback/")
# def callback():
#     discord.callback()
#     user = discord.fetch_user()
#     welcome_user(user)
#     return redirect(url_for("index.index"))

# @app.errorhandler(Unauthorized)
# def redirect_unauthorized(e):
#     return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)