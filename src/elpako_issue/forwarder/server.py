import os, time, threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_url_path="/welcome/static")

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

visitor_data_lock = threading.Lock()
visitor_data = {}

cors = CORS(
    app,
    resources={
        r"/*": {"origins": ["https://www.yoyo.lt", "https://127.0.0.1"]}
    }
)

@app.route("/welcome/", methods=["GET"])
def welcome():
    with visitor_data_lock:
        visitor_data.clear()

    return render_template("welcome.html")

@app.route("/welcome/start_session", methods=["GET"])
def start_session():
    with visitor_data_lock:
        visitor_data.clear()

    return jsonify({})

@app.route("/welcome/wait_for_the_visitor", methods=["GET"])
def wait_for_the_visitor():
    started = time.time()

    while True:
        with visitor_data_lock:
            if set(visitor_data.keys()) == {'visitor_name', 'certificate', 'name', 'issuer', 'validTo'}:
                break

        time.sleep(0.1)

        if time.time() - started > 300:
            return jsonify({ "success": False, "message": "Timed out"})

    response = None

    with visitor_data_lock:
        response = { "success": True } | visitor_data

    return jsonify(response)

@app.route("/welcome/submit_visitor_name", methods=["POST"])
def submit_visitor_name():
    request_params = request.get_json()

    print(f"Got visitor name: {request_params['visitor_name']}")

    with visitor_data_lock:
        visitor_data.clear()
        visitor_data['visitor_name'] = request_params['visitor_name']

    return jsonify({
        "success": True
    })

@app.route("/welcome/submit_certificate", methods=["POST"])
def submit_certificate():
    request_params = request.get_json()

    print(f"Got certificate: {request_params['name']} / {request_params['issuer']} / {request_params['validTo']}")

    with visitor_data_lock:
        visitor_data['certificate'] = request_params['certificate']
        visitor_data['name'] = request_params['name']
        visitor_data['issuer'] = request_params['issuer']
        visitor_data['validTo'] = request_params['validTo']

    return jsonify({
        "success": True
    })

@app.route("/welcome/dtbs", methods=["get"])
def dtbs():
    global visitor_data

    started = time.time()

    result = {}

    while True:
        with visitor_data_lock:
            if 'dtbs' in visitor_data:
                result['dtbs'] = visitor_data['dtbs']
                break

        time.sleep(0.1)

        if time.time() - started > 300:
            return jsonify({ "success": False, "message": "Timed out"})

    return jsonify(result)

@app.route("/welcome/sign_dtbs", methods=["post"])
def sign_dtbs():
    global visitor_data

    result = {}
    started = time.time()

    request_params = request.get_json()
    print(f"Got dtbs to sign: {request_params['dtbs']}")

    with visitor_data_lock:
        visitor_data['dtbs'] = request_params['dtbs']

    while True:
        with visitor_data_lock:
            if 'result' in visitor_data:
                result['result'] = visitor_data['result']
                break

        time.sleep(0.1)

        if time.time() - started > 300:
            return jsonify({ "success": False, "message": "Timed out"})

    return jsonify(result)

@app.route("/welcome/submit_result", methods=["post"])
def submit_result():
    global visitor_data

    request_params = request.get_json()
    print(f"Got the signature: {request_params['result']}")

    with visitor_data_lock:
        visitor_data['result'] = request_params['result']

    return jsonify({})
