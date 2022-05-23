import traceback
import requests
from requests.exceptions import HTTPError


def main():
    # define default value
    url = 'http://0.0.0.0:9001'
    file_name = 'temp_file.txt'
    bucket_name = 'test-bucket-1'
    chunk_size = 8192
    data = {'key': file_name}

    # endpoints
    list_buckets = '/api/v1/buckets/list'
    list_objects = '/api/v1/%s/object/list'
    get_object = '/api/v1/bucket/%s/object/%s'
    file_path = '/home/user/Desktop/sber/mtls/data/'

    # certs
    ca_path = '/home/user/Desktop/sber/mtls/certs/rootCA.pem'
    cert = ('/home/user/Desktop/sber/mtls/certs/client2.pem',
            '/home/user/Desktop/sber/mtls/certs/client2.key'
            )

    # request for getting list buckets from s3 server
    with requests.post(url + list_buckets, verify=ca_path, cert=cert, data=data) as r:
        print(f'list buckets: {r}')

    # # request for getting list objects in bucket from s3 server
    # with requests.post(url + list_objects % (bucket_name), verify=ca_path, cert=cert, data=data) as r:
    #     print(f'list objects: {r}')
    #
    # # request for reading file in stream mode from s3 server
    # with requests.post(url + get_object % (bucket_name, file_name), verify=ca_path, cert=cert, stream=True, data=data) as r:
    #     # writing to local file from response data
    #     with open(file_path + file_name, 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=chunk_size):
    #             f.write(chunk)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
        print(f'Traceback: {traceback.format_exc()}')