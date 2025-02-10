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
    s3 = boto3.resource('s3')
    kids_data = event.get('kids')

    for kid in kids_data:
        file_name = kid['name'].lower() + "_school_calendar.ics"
        logger.info('file name: ' + file_name)

        obj = s3.Object(bucket_name, file_name)
        body = obj.get()['Body'].read().decode('utf-8') 
        logger.info('read calendar file from S3 bucket')

        # load calendar from body
        cal = icalendar.Calendar.from_ical(body)

        # cal = icalendar.Calendar.from_ical(open('district_calendar.ics').read())

        # create a new calendar
        kid_encores = icalendar.Calendar()
        kid_encores.add('prodid', '-//Family Encores//EN')
        kid_encores.add('version', '2.0')
       
        # iterate over calendar events
        for event in cal.walk('vevent'):    
            school_event = event

            # family_event['SUMMARY'] = 'Sofya: ' + sofya_encore[event.get('summary')] + ' | Mark: ' + mark_encore[event.get('summary')] 
            encore_day = event.get('summary')

            for encore in kid['encores']:
                if encore['day'] == encore_day:
                    # print("Today's encore is: " + encore['classes'])
                    school_event['SUMMARY'] = encore['day'] + ': ' + encore['classes']

            kid_encores.add_component(school_event)

        # write kid_encores calendar to S3 bucket
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name, kid['name'].lower() + '_encores.ics')
        obj.put(Body=kid_encores.to_ical())
        logger.info('Wrote family encores calendar to S3 bucket')