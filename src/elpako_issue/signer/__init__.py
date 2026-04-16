import os, pathlib
from elpako_issue.signer.server import app

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
        processes=1,
        use_reloader=True,
        use_debugger=True
    )
