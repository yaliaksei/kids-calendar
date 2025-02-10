# create AWS labmda with lambda_handler as handler
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # delete calendar file from S3 bucket
    bucket_name = os.environ['BUCKET_NAME']
    s3 = boto3.resource('s3')

    kids_data = event.get('kids')
    for kid in kids_data:
        file_name = kid['name'].lower() + "_school_calendar.ics"
        obj = s3.Object(bucket_name, file_name)
        obj.delete()
        logger.info('deleted calendar file from S3 bucket')

