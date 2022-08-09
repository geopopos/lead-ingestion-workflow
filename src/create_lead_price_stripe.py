from tkinter import W
import stripe, os, requests, json

from urllib import parse

stripe_api_key = os.environ.get('STRIPE_API_KEY')
ppl_api_url ="https://e6b1hc9rfg.execute-api.us-east-1.amazonaws.com"

if os.environ.get('IS_LOCAL') == 'true':
    stripe_api_key = os.environ.get('STRIPE_TEST_API_KEY')
    ppl_api_url = "http://localhost:2000"

if os.environ.get('STAGE') == 'dev':
    stripe_api_key = os.environ.get('STRIPE_TEST_API_KEY')

def create_lead_price_stripe(event, context):
    stripe.api_key = stripe_api_key
    product_id = event.get('product').get("id")
    price = stripe.Price.create(
        unit_amount=5000,
        currency="usd",
        product=product_id
    )

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "price_id": price.id,
    }

    response = requests.request("PUT", f"{ppl_api_url}/lead/{parse.quote(event.get('pk'))}", data=json.dumps(body), headers=headers)

    event['price'] = price

    return event