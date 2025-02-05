# create AWS labmda with lambda_handler as handler
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.info('context{}'.format(context))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Process Lambda!')
    }