import os
import boto3
import logging
import traceback

logging.basicConfig(filename='test_boto3.log', encoding='utf-8', level=logging.DEBUG)


def log_print(message):
    logger.debug(message)
    print(message)


def main():
    # const
    region_name = 'local'
    bucket = 'boto3_test'
    key = 'hello-world.txt'
    file_name = './hello-world.txt'
    aws_access_key_id='minioadmin'
    aws_secret_access_key='minioadmin'
    expiresin_presigned_url = 60 ** 2
    endpoint_url = 'https://127.0.0.1:9000/'

    # setup boto3
    log_message = 'setup boto3 session'
    logger.debug(log_message)
    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url=endpoint_url,
                            region_name=region_name,
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key
                            )

    # create test bucket
    log_message = f'create bucket: {bucket}'
    log_print(log_message)
    client.create_bucket(Bucket=bucket)

    # get list buckets
    response = client.list_buckets()
    log_message = f'buckets list: {response}'
    log_print(log_message)

    # put test object/file to s3
    log_message = f'put test object: key: {key}, bucket: {bucket}'
    log_print(log_message)
    client.put_object(Bucket=bucket,
                      Key=key,
                      Body=b'Hello, World!',
                    )

    # get test object/file from s3
    log_message = f'get test object: key: {key}, bucket: {bucket}, file_name: {file_name}'
    log_print(log_message)
    client.download_file(bucket, key, file_name)

    # get presigned url on object/file
    object_url = client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiresin_presigned_url
    )

    log_message = f'presigned_url: {object_url}, key: {key}, bucket: {bucket}, expiresin: {expiresin_presigned_url}'
    log_print(log_message)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log_message = f'error: {e}'
        log_print(log_message)

        log_message = f'traceback: {traceback.format_exc()}'
        log_print(log_message)
