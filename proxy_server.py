import traceback

import const
import config
from PeerCertWSGIRequestHandler import PeerCertWSGIRequestHandler

import ssl
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def handler():
    try:
        client_cert = request.environ['client_cert']

        print(client_cert.get_subject())
    except Exception as e:
        print(traceback.format_exc())

    return const.RESPONSE_STATUS_OK


if __name__ == "__main__":
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=config.CA_CERT)

    ssl_context.load_cert_chain(certfile=config.APP_CERT, keyfile=config.APP_KEY, password=config.APP_KEY_PASSWORD)
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    app.run(ssl_context=ssl_context, request_handler=PeerCertWSGIRequestHandler)
