import os
import logger
import traceback
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

logging.basicConfig(filename='test_pyspark.log', encoding='utf-8', level=logging.DEBUG)


def log_print(message):
    print(message)
    logger.debug(message)


def main():
    # const
    bucket = 'pyspark_test'
    file_name_csv = 'test_table.csv'
    aws_access_key_id='minioadmin'
    aws_secret_access_key='minioadmin'
    endpoint_url = 'https://127.0.0.1:9000/'

    os.environ['PYSPARK_SUBMIT_ARGS'] = \
        '-- packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3 pyspark-shell'

    # setup spark
    log_message = 'setup spark'
    log_print(log_message)
    conf = SparkConf() \
        .set('spark.executor.extraJavaOptions', '-Dcom.amazonaws.services.s3.enableV4 = true') \
        .set('spark.driver.extraJavaOptions', '-Dcom.amazonaws.services.s3.enableV4 = true') \
        .setAppName('pyspark_aws') \
        .setMaster('local[*]')

    sc = SparkContext(conf=conf)
    sc.setSystemProperty('com.amazonaws.services.s3.enableV4', 'true')

    # setup hadoop conf with s3
    log_message = 'setup hadoop conf with s3'
    log_print(log_message)
    hadoopConf = sc._jsc.hadoopConfiguration()
    hadoopConf.set('fs.s3a.access.key', aws_access_key_id)
    hadoopConf.set('fs.s3a.secret.key', aws_secret_access_key)
    hadoopConf.set('fs.s3a.endpoint', endpoint_url)
    hadoopConf.set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')

    # create spark session
    log_message = 'create spark session'
    log_print(log_message)
    spark = SparkSession(sc)

    # read file (csv) from local
    test_df = spark.read.csv(f'./{file_name_csv}', header=True, inferSchema=True)
    result = test_df.show(5)
    log_message = f'read file (csv), \n {result}'
    log_print(log_message)

    # upload file to s3
    log_message = f'upload file to s3: bucket: {bucket}, file_name_csv: {file_name_csv}'
    log_print(log_message)
    test_df.write.format('csv').option('header', 'true').save(f's3a://{bucket}/{file_name_csv}',
                                                              mode='overwrite')

    # read file (csv) from s3
    test_s3_df = spark.read.csv(f's3a://{bucket}/{file_name_csv}', header=True, inferSchema=True)
    result = test_s3_df.show(5)
    log_message = f'read file from s3: bucket: {bucket}, file_name_csv: {file_name_csv},\n{result}'
    log_print(log_message)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log_message = f'error: {e}'
        log_print(log_message)

        log_message = f'traceback: {traceback.format_exc()}'
        log_print(log_message)
