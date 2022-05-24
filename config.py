APP_KEY = '/opt/mtls/certs/client1.key'
APP_KEY_PASSWORD = None
APP_CERT = '/opt/mtls/certs/client1.pem'
CA_CERT = './certs/rootCA.pem'

REDIRECT_HOST = 'minio:9000'
S3_HOST = 'http://minio1:9000'

AWS_ACCESS_KEY_ID = 'minioadmin'
AWS_SECRET_ACCESS_KEY = 'minioadmin'
REGION_NAME = 'local'

LIST_BUCKETS_ENDPOINT = '/api/v1/buckets/list'
GET_OBJECT_ENDPOINT = '/api/v1/bucket/<bucket>/object/<object>'

DOWNLOAD_DIR = '/opt/mtls/data/'

LOGS_PATH = '/opt/mtls/logs/debug.log'