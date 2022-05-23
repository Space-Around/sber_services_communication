# Proxy Server
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Providing communication between Keycloak, SberECM core and S3 server (Minio) via proxy server in Docker. Auth to proxy server via mTLS protocol.

---

## Installation
```sh 
cd path/to/project
chmod +x setup.sh
./setup.sh
```

### Start up
```sh 
./start.sh
```
---
## Test communications between services

Check folder ```/tests``` and run Python scripts for testing


##### Get list buckets

```sh
curl --cacert certs/rootCA.pem \
    --cert certs/client2.pem \
    --key certs/client2.key \
    https://127.0.0.1:5000/api/v1/buckets/list \
    -vvv
```

##### Download file
```
curl --cacert certs/rootCA.pem \
    --cert certs/client2.pem \
    --key certs/client2.key \
    https://127.0.0.1:5000/api/v1/bucket/test-bucket-1/object/temp_file.txt \
    --output /opt/mtls/data/t.txt \
    -vvv
```
---

## Docker Compose
```sh 
cd path/to/project
docker-compose build
docker-comose up -d
```