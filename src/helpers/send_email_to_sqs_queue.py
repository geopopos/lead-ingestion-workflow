from string import Template
import requests, json

def send_email_to_sqs_queue(logger, sqs_email_client, email_queue_url, message_subject, message_body, roofing_contractor):
    # create notification for sms
    notification = {
        "notification_type": "lead",
        "message_subject": message_subject,
        "message_body": message_body,
        "to_address": roofing_contractor.get('Email')
    }
    # create task in sqs sms
    try:
        task = sqs_email_client.send_message(
            QueueUrl=email_queue_url, 
            MessageBody=json.dumps(notification)
            )
        logger.info(f"task: {task}")
        message = f"task: {task}"
        status_code = 200
    except Exception as e:
        logger.exception('Sending message to SQS queue failed!')
        message = str(e)
        status_code = 500
    

    return {"statusCode": status_code, "body": message}