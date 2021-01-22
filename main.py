from flask import Flask, Blueprint
from routes.compare import compare_blueprint
from routes.index import index_blueprint

app = Flask(__name__)
# Register the blueprint for each route
app.register_blueprint(index_blueprint)
app.register_blueprint(compare_blueprint)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)