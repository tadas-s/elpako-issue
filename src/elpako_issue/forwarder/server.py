from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(
    app,
    resources={
        r"/*": {"origins": ["https://www.yoyo.lt"]}
    }
)

@app.route("/welcome/", methods=["GET"])
def welcome():
    return "<h1>Sveiki!</h1>"
