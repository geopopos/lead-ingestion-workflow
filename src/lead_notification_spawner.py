from email import message
import os, json, requests, boto3, logging
from string import Template
from helpers import send_sms_to_sqs_queue, send_email_to_sqs_queue

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sqs_client = boto3.client('sqs')

ppl_api_url ="https://e6b1hc9rfg.execute-api.us-east-1.amazonaws.com"

if os.environ.get('IS_LOCAL') == 'true':
    ppl_api_url = "http://localhost:2000"


def lead_notification_spawner(event, context):
    # for each record, create a notification
    # for each notification, create a task in sqs
    sms_queue_url = os.environ.get('SQS_SMS_QUEUE_URL')
    email_queue_url = os.environ.get('SQS_EMAIL_QUEUE_URL')

    # for each record, create a notification
    # for each notification, create a task in sqs

    # get all lead data for notification
    city = event.get('geocode_address').get('city')    
    zip_code = event.get('geocode_address').get('zip_code')
    state = event.get('geocode_address').get('state')
    project_timeline = event.get('data').get('project_timeline')
    project_scope = event.get('data').get('project_scope')
    payment_link = event.get('payment_link').get('url')

    # create lead notification message_subject
    message_subject = Template("New $state Lead Alert! 🚨")

    # create lead notification message_body
    message_body = Template("""🚨New $state Lead Alert! 🚨
    City: $city
    Zip Code: $zip_code
    Project Scope: $project_scope
    Project Timeline: $project_timeline
    You Can Purchase The Lead Below 👇 [First Come First Serve]
        $payment_link

    NOTE: Make sure to use the email you signed up with so there is no delay in getting your lead: $contractor_email""")

    # scan for all records in dynamodb with ROOFER sort key
    response = requests.request("GET", f"{ppl_api_url}/roofer/")
    roofing_contractors = json.loads(response.text)

    for roofing_contractor in roofing_contractors:
        sms_response = send_sms_to_sqs_queue.send_sms_to_sqs_queue(logger, sqs_client, sms_queue_url, message_body.substitute(city=city, zip_code=zip_code, state=state, project_scope=project_scope, project_timeline=project_timeline, payment_link=payment_link, contractor_email=roofing_contractor.get('Email')), roofing_contractor)

        email_response = send_email_to_sqs_queue.send_email_to_sqs_queue(logger, sqs_client, email_queue_url, message_subject=message_subject.substitute(state=state), message_body=message_body.substitute(city=city, zip_code=zip_code, state=state, project_scope=project_scope, project_timeline=project_timeline, payment_link=payment_link, contractor_email=roofing_contractor.get('Email')), roofing_contractor=roofing_contractor)

    return {"statusCode": 200, "body": json.dumps({"sms_response": sms_response, "email_response": email_response})}