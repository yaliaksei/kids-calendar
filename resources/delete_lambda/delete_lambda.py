# create AWS labmda with lambda_handler as handler
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # delete calendar file from S3 bucket
    bucket_name = os.environ['BUCKET_NAME']
    file_name = "district_calendar.ics"
    s3 = boto3.resource('s3')
    
    obj = s3.Object(bucket_name, file_name)
    obj.delete()
    logger.info('deleted calendar file from S3 bucket')

