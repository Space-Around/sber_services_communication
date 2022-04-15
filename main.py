import traceback

import config

import ssl
from PeerCertWSGIRequestHandler import PeerCertWSGIRequestHandler
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def handler():
    print(request.environ.keys())
    print(dir(request.environ['SSL_CLIENT_CERT']))
    print(request.environ['SSL_CLIENT_CERT'])

    return '200', 200


if __name__ == "__main__":
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=config.CA_CERT)

    ssl_context.load_cert_chain(certfile=config.APP_CERT, keyfile=config.APP_KEY, password=config.APP_KEY_PASSWORD)
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    app.run(ssl_context=ssl_context, request_handler=PeerCertWSGIRequestHandler)
