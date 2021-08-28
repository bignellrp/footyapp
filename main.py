from flask import Flask, Blueprint
from services.lookup import lookup
import pkgutil
import sys
import bot #Used even though shows as not accessed

app = Flask(__name__)

##Register the blueprint for each route
##https://stackoverflow.com/questions/26550180/flask-blueprint-attributeerror-module-object-has-no-attribute-name-error
EXTENSIONS_DIR = "routes"
modules = pkgutil.iter_modules(path=[EXTENSIONS_DIR])
for loader, mod_name, ispkg in modules: 
    if mod_name not in sys.modules:
        loaded_mod = __import__(EXTENSIONS_DIR+"."+mod_name, fromlist=[mod_name])
    for obj in vars(loaded_mod).values():
        if isinstance(obj, Blueprint):
            app.register_blueprint(obj)

##Import Secret Key for Session Pop
app.secret_key = lookup("session")

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)