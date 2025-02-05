# create AWS labmda with lambda_handler as handler
import boto3
import logging
import icalendar
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # read district_calendar.ics from S3 bucket
    bucket_name = os.environ['BUCKET_NAME']
    file_name = "district_calendar.ics"
    s3 = boto3.resource('s3')

    obj = s3.Object(bucket_name, file_name)
    body = obj.get()['Body'].read().decode('utf-8') 
    logger.info('read calendar file from S3 bucket')

    # load calendar from body
    cal = icalendar.Calendar.from_ical(body)

    # cal = icalendar.Calendar.from_ical(open('district_calendar.ics').read())

    # create a new calendar
    family_encores = icalendar.Calendar()
    family_encores.add('prodid', '-//Family Encores//EN')
    family_encores.add('version', '2.0')

    mark_encore = {
        'A' : 'Music',
        'B' : 'Art',
        'C' : 'Gym',
        'D' : 'iDesign',
        'E' : 'Gym',
        'F' : 'Library'
    }

    sofya_encore = {
        'A' : 'Gym, Health',
        'B' : 'Spanish, Engineering',
        'C' : 'Art, Band',
        'D' : 'Gym, Health',
        'E' : 'Spanish, Engineering',
        'F' : 'Art, Band'
    }

    # iterate over calendar events
    for event in cal.walk('vevent'):    
        family_event = event
        family_event['SUMMARY'] = 'Sofya: ' + sofya_encore[event.get('summary')] + ' | Mark: ' + mark_encore[event.get('summary')] 

        family_encores.add_component(event)

    # write family_encores calendar to S3 bucket
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, 'kids_encores.ics')
    obj.put(Body=family_encores.to_ical())
    logger.info('wrote family encores calendar to S3 bucket')