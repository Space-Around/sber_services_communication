import urllib3
from minio import Minio
from minio.error import S3Error
import ssl

def main():
    # const
    bucket_name = 'test-bucket-1'
    endpoint_url = 'minio1:9000'
    access_key = 'minioadmin'
    secret_key = 'minioadmin'
    upload_file_path = './data/img.png'
    file_name = 'img2.png'

    # setup ssl context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # context.load_verify_locations('path/to/cabundle.pem')

    # setup proxy http client
    http_client = urllib3.PoolManager(
            "https://127.0.0.1:5000/",
            timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
            cert_reqs="CERT_REQUIRED",
            retries=urllib3.Retry(
                total=5,
                backoff_factor=0.2,
                status_forcelist=[500, 502, 503, 504],
            ),
        )

    # setup s3 (minio) client
    client = Minio(
        endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=True,
        http_client=http_client
    )

    found = client.bucket_exists(bucket_name)

    if not found:
        client.make_bucket(bucket_name)
    else:
        print(f"Bucket '{bucket_name}' already exists")

    client.fput_object(bucket_name, file_name, upload_file_path)

    print(
        f"'{upload_file_path}' is successfully uploaded as "
        f"object '{file_name}' to bucket '{bucket_name}'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)