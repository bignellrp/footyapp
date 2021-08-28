from flask import Flask
from services.lookup import lookup
from routes import *
import os
import bot #Used even though shows as not accessed

app = Flask(__name__)

##Register the blueprint for each route

for file in os.listdir("routes"):
    if file.startsswith("__init__"):
        pass
    elif file.endswith(".py"):
        name = file[:-3]
        app.register_blueprint(f"{name}_blueprint")

#app.register_blueprint(index_blueprint)
#app.register_blueprint(compare_blueprint)
#app.register_blueprint(leaderboard_blueprint)
#app.register_blueprint(stats_blueprint)
#app.register_blueprint(result_blueprint)
#app.register_blueprint(score_blueprint)

##Import Secret Key for Session Pop
app.secret_key = lookup("session")

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)