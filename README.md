<h1>Proxy Server</h1>
<hr/>

<h2>Setup:</h2>
1. ```chmod +x setup.sh```
2. ```./setup.sh```

<h2>Start:</h2>
```./start.sh```
<hr/>
<h2>Test communications between services:</h2>

Check folder ```/tests``` and run Python scripts for testing

<h3>cURL test:</h3>
<h4>Get list buckets</h4>
```
curl --cacert certs/rootCA.pem \
    --cert certs/client2.pem \
    --key certs/client2.key \
    https://127.0.0.1:5000/api/v1/buckets/list \
    -vvv
```

<h4>Download file</h4>
```
curl --cacert certs/rootCA.pem \
    --cert certs/client2.pem \
    --key certs/client2.key \
    https://127.0.0.1:5000/api/v1/bucket/test-bucket-1/object/temp_file.txt \
    --output /opt/mtls/data/t.txt \
    -vvv
```
<hr/>

<h2>Docker</h2>
1. ```cd path/to/project```
2. ```docker-compose build .```
3. ```docker-comose up -d```