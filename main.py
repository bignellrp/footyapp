from quart import Quart, url_for, redirect
from routes.compare import compare_blueprint
from routes.index import index_blueprint
from routes.leaderboard import leaderboard_blueprint
from routes.stats import stats_blueprint
from routes.result import result_blueprint
from routes.score import score_blueprint
import bot
import json
from threading import Thread

app = Quart(__name__)

##Register the blueprint for each route
app.register_blueprint(index_blueprint)
app.register_blueprint(compare_blueprint)
app.register_blueprint(leaderboard_blueprint)
app.register_blueprint(stats_blueprint)
app.register_blueprint(result_blueprint)
app.register_blueprint(score_blueprint)

##Quart session needs a key.
##https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-files
app.config.from_pyfile('config.py')
app.config['SESSION_TYPE'] = 'filesystem'

##Get keys from token json
path_to_token = "./services/tokens.json"
with open(path_to_token, "r") as handler:
    info = json.load(handler)

def run():
  app.run(host="127.0.0.1", debug=False, port=5000)
  #app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
  #bot.run(token) #ValueError: set_wakeup_fd only works in main thread

# t = Thread(target=run)
# t.start()
# bot.run(token)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)
    #t = Thread(target=run)
    #t.start()
    bot.bot.run(bot.token)