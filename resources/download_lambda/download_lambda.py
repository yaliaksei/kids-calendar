# create AWS labmda with lambda_handler as handler
import boto3
import json
import logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.info('context{}'.format(context))

    # get the bucket name from Environment
    bucket_name = os.environ['BUCKET_NAME']

    # download file fron the url and store it in the bucket
    url = os.environ['SCHOOL_CALENDAR_URL']
    file_name = "disrict_calendar.ics"

    try:
        # Download file from URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Upload directly to S3 from memory
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=response.content
        )
        
        logger.info('File {} downloaded and stored in bucket {}'.format(file_name, bucket_name))
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully downloaded and uploaded school calendar file')
        }
    
    except requests.exceptions.RequestException as e:
        logger.error('Error downloading file: {}'.format(str(e)))
        return {
            'statusCode': 500,
            'body': json.dumps('Error downloading file')
        }
    except Exception as e:
        logger.error('Error: {}'.format(str(e)))
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing request')
        }

    