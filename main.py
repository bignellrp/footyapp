from flask import Flask, Blueprint
from routes.compare import compare_blueprint
from routes.index import index_blueprint

app = Flask(__name__)

app.register_blueprint(compare_blueprint, url_prefix='/compare')
app.register_blueprint(index_blueprint, url_prefix='/')

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000)