#!/bin/sh

echo 'verify proxy server cert...'
openssl verify -verbose -CAfile certs/rootCA.pem cert/sclient1.pem

echo 'starting proxy server...'
python proxy_server.py