import requests, os, json

from urllib import parse

ppl_api_url ="https://e6b1hc9rfg.execute-api.us-east-1.amazonaws.com"

if os.environ.get('IS_LOCAL') == 'true':
    ppl_api_url = "http://localhost:2000"

def get_full_address(event, context):
    address = event.get("data").get("address")
    address_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={os.environ.get('GOOGLE_API_KEY')}"
    response = requests.get(address_url)
    event['geocode_address'] = {"geocode_address": response.json().get('results')[0].get('formatted_address')}

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "geocode_address": response.json().get('results')[0].get('formatted_address')
    }

    lead_url = f"{ppl_api_url}/lead/{parse.quote(event.get('pk'))}"

    requests.request("PUT", lead_url, data=json.dumps(body), headers=headers)

    return event