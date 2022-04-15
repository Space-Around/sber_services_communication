from minio import Minio
from minio.error import S3Error


def main():
    bucket_name = 'test-bucket-1'
    endpoint_url = 'minio1:9000'
    access_key = 'minioadmin'
    secret_key = 'minioadmin'
    upload_file_path = './data/img.png'
    file_name = 'img.png'

    client = Minio(
        endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=False
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