import json
import os, pathlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from base64 import b64encode, b64decode
from hashlib import sha256
import requests
# from asn1crypto.x509 import Certificate

FORWARDER_BASE_URL="https://www.yoyo.lt/welcome"

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "https://api.elpako.lt"}})

visitor_data = {}

@app.route("/", methods=["GET"])
def main_index():
    return "<p>Parašo serveris/tarpininkas veikia.</p>"

#
# Javascript snippet to be used in api.elpako.lt sign in page console:
#
#     fetch('https://127.0.0.1:38888/wait_for_the_visitor').then(function(response) {
#       console.info(response);
#       if (response.status == 200) { startAuthentication(); }
#     });
#
@app.route("/wait_for_the_visitor", methods=["GET"])
def wait_for_the_visitor():
    global visitor_data

    r = requests.get(f"{FORWARDER_BASE_URL}/wait_for_the_visitor")

    visitor_data = r.json()

    return jsonify({
        "success": r.status_code == 200
    })

@app.route("/Handshake/Browser", methods=["GET"])
def handshake_browser():
    global visitor_data

    return visitor_data['visitor_name']

# GET /Signing/SelectCertificate?childName=jonas&sessionId=null&store=usb2&purpose=authentication&withLog=false
@app.route("/Signing/SelectCertificate", methods=["GET"])
def signing_select_certificate():
    global visitor_data

    return jsonify({
        "certificate": visitor_data['certificate'],
        "name": visitor_data['name'],
        "issuer": visitor_data['issuer'],
        "validTo": visitor_data['validTo']
    })

@app.route("/Signing/Sign", methods=["POST"])
def signing_sign():
    global visitor_data

    dtbs = request.json['dtbs']

    r = requests.post(
        f"{FORWARDER_BASE_URL}/sign_dtbs",
        json={ 'dtbs': dtbs }
    )

    return jsonify({
        "result": r.json()['result']
    })

def run():
    from werkzeug.serving import run_simple

    ssl_context = (
        os.path.join(pathlib.Path(__file__).parent, 'ssl', 'cert.pem'),
        os.path.join(pathlib.Path(__file__).parent, 'ssl', 'key.pem'),
    )

    run_simple(
        hostname='127.0.0.1',
        port=38888,
        application=app,
        ssl_context=ssl_context,
        threaded=False,
        processes=1
    )
