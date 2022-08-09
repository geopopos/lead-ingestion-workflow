import os, requests, json
from string import Template

def send_sms_to_sqs_queue(logger, sqs_client, sms_queue_url, event):
    # for each record, create a notification
    # for each notification, create a task in sqs

    # get all lead data for notification
    city = event.get('geocode_address').get('city')    
    zip_code = event.get('geocode_address').get('zip_code')
    state = event.get('geocode_address').get('state')
    project_timeline = event.get('data').get('project_timeline')
    project_scope = event.get('data').get('project_scope')
    payment_link = event.get('payment_link').get('url')

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
        # create notification for sms
        notification = {
            "notification_type": "lead",
            "message_body": message_body.substitute(city=city, zip_code=zip_code, state=state, project_scope=project_scope, project_timeline=project_timeline, payment_link=payment_link, contractor_email=roofing_contractor.get('Email')),
            "to_number": roofing_contractor.get('Phone')
        }
        # create task in sqs sms
        try:
            task = sqs_client.send_message(
                QueueUrl=sms_queue_url, 
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