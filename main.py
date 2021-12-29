from flask import redirect, url_for
import bot #Used even though shows as not accessed
from init import create_app
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = create_app()
discord = DiscordOAuth2Session()

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)