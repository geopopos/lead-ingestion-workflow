import requests, os, json

from urllib import parse

ppl_api_url ="https://e6b1hc9rfg.execute-api.us-east-1.amazonaws.com"

if os.environ.get('IS_LOCAL') == 'true':
    ppl_api_url = "http://localhost:2000"

def get_full_address(event, context):
    address = event.get("data").get("address")
    address_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={os.environ.get('GOOGLE_API_KEY')}"
    response = requests.get(address_url)

    address_components = json.loads(response.text)['results'][0]['address_components']

    ac_match = list(filter(lambda ac:"locality" in ac['types'], address_components))
    city = ac_match[0]['long_name'] if ac_match else None

    ac_match = list(filter(lambda ac:"administrative_area_level_1" in ac['types'], address_components))
    state = ac_match[0]['long_name'] if ac_match else None

    ac_match = list(filter(lambda ac:"postal_code" in ac['types'], address_components))
    zip_code = ac_match[0]['long_name'] if ac_match else None

    full_address = response.json().get('results')[0].get('formatted_address')

    event['geocode_address'] = {"geocode_address": full_address, "city": city, "state": state, "zip_code": zip_code}

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "geocode_address": response.json().get('results')[0].get('formatted_address')
    }

    lead_url = f"{ppl_api_url}/lead/{parse.quote(event.get('pk'))}"

    response = requests.request("PUT", lead_url, data=json.dumps(body), headers=headers)

    return event