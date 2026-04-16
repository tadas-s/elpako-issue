from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
cors = CORS(
    app,
    resources={
        r"/*": {"origins": ["https://www.yoyo.lt"]}
    }
)

@app.route("/welcome/", methods=["GET"])
def welcome():
    return "<h1>Sveiki!</h1>"
