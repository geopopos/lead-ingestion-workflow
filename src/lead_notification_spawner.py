import os, json, requests, boto3, logging
from string import Template
from helpers import send_sms_to_sqs_queue

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

    return send_sms_to_sqs_queue.send_sms_to_sqs_queue(logger, sqs_client, sms_queue_url, event)