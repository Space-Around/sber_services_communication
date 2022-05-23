import os
import traceback
import logging
from typing import Union

import const
import config
from PeerCertWSGIRequestHandler import PeerCertWSGIRequestHandler

import ssl
import boto3
import requests
from flask import Flask, request, Response, send_file, jsonify, after_this_request

app = Flask(__name__)
logging.basicConfig(filename=config.LOGS_PATH, level=logging.DEBUG)


@app.route(config.LIST_BUCKETS_ENDPOINT)
def list_buckets() -> Union[tuple[Response, int], tuple[str, int]]:
    try:
        debug_info = f'Handle list buckets, ip: {request.remote_addr}'
        logging.debug(debug_info)
        # client_cert = request.environ['client_cert']

        # request to get jwt from keycloak

        # request to check if user has access to file from SberECM Core

        session = boto3.session.Session()
        client = session.client('s3',
                                endpoint_url=config.S3_HOST,
                                region_name=config.REGION_NAME,
                                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
                                )
        # request to getting file from s3 server
        list_buckets = client.list_buckets()

        debug_info = f'buckets: {list_buckets}, ip: {request.remote_addr}'
        logging.debug(debug_info)

        return jsonify(list_buckets), 200

    except Exception as e:
        logging.debug(traceback.format_exc())

    return const.RESPONSE_STATUS_OK


@app.route(config.GET_OBJECT_ENDPOINT)
def get_object(bucket: str, object: str) -> Union[tuple[Response, int], tuple[str, int]]:
    try:
        debug_info = f'Handle get object, ip: {request.remote_addr}'
        logging.debug(debug_info)

        # client_cert = request.environ['client_cert']

        # request to get jwt from keycloak

        # request to check if user has access to file from SberECM Core

        # request to getting file from s3 server
        session = boto3.session.Session()
        client = session.client('s3',
                                endpoint_url=config.S3_HOST,
                                region_name=config.REGION_NAME,
                                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
                                )

        debug_info = f'bucket: {bucket}, object: {object}, path: {config.DOWNLOAD_DIR + object}, ip: {request.remote_addr}'
        logging.debug(debug_info)

        # create temp file
        open(config.DOWNLOAD_DIR + object, "w").close()

        # client.download_file(bucket, object, config.DOWNLOAD_DIR + object)
        with open(config.DOWNLOAD_DIR + object, 'wb') as f:
            try:
                client.download_fileobj(bucket, object, f)
            except Exception as e:
                debug_ingo = traceback.format_exc()
                logging.debug(debug_ingo, e)

        debug_ingo = f'File successfully download from s3 server, ip: {request.remote_addr}'
        logging.debug(debug_ingo)

        debug_ingo = f'File sending, ip: {request.remote_addr}'
        logging.debug(debug_ingo)

        # delete user file from local after sending it
        @after_this_request
        def remove_file(response):
            try:
                os.remove(config.DOWNLOAD_DIR + object)
            except Exception as e:
                error_info = f'Error removing file handle, file: {config.DOWNLOAD_DIR + object}, ip: {request.remote_addr}'
                logging.error(error_info, e)
            return response

        return send_file(config.DOWNLOAD_DIR + object, attachment_filename=object)

    except Exception as e:
        error_info = traceback.format_exc()
        logging.error(error_info, e)

    return const.RESPONSE_STATUS_OK


if __name__ == "__main__":
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=config.CA_CERT)

    ssl_context.load_cert_chain(certfile=config.APP_CERT, keyfile=config.APP_KEY, password=config.APP_KEY_PASSWORD)
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    app.run(ssl_context=ssl_context, request_handler=PeerCertWSGIRequestHandler)
