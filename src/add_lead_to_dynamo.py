import json, requests, os

ppl_api_url ="https://e6b1hc9rfg.execute-api.us-east-1.amazonaws.com"

if os.environ.get('IS_LOCAL') == 'true':
    ppl_api_url = "http://localhost:2000"

def add_lead_to_dynamo(event, context):
    body = {
        "full_name": event.get("full_name"),
        "email": event.get("email"),
        "phone": event.get("phone"),
        "date_created": event.get("date_created"),
        "address": event.get("full_address"),
        "project_scope": event.get("Project Scope"),
        "project_timeline": event.get("Project Timeline")
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("POST", f"{ppl_api_url}/lead", data=json.dumps(body), headers=headers)
    return json.loads(response.text)