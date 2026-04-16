import os
import werkzeug
from elpako_issue.forwarder.server import app

def run():
    from werkzeug.serving import run_simple

    run_simple(
        hostname='127.0.0.1',
        port=4000,
        application=app,
        threaded=False,
        processes=1
    )
