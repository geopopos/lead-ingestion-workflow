import stripe, os, requests, json

from urllib import parse

stripe_api_key = os.environ.get('STRIPE_API_KEY')
ppl_api_url ="https://e6b1hc9rfg.execute-api.us-east-1.amazonaws.com"

if os.environ.get('IS_LOCAL') == 'true':
    stripe_api_key = os.environ.get('STRIPE_TEST_API_KEY')
    ppl_api_url = "http://localhost:2000"

if os.environ.get('STAGE') == 'dev':
    stripe_api_key = os.environ.get('STRIPE_TEST_API_KEY')

def create_payment_link(event, context):
    # create a payment link with a price and and quantity
    stripe.api_key = stripe_api_key
    price_id = event.get("price").get("id")
    payment_link = stripe.PaymentLink.create(
        line_items=[
            {
                "price": price_id,
                "quantity": 1
            }
        ]
    )
    
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "payment_link_id": payment_link.id,
    }

    response = requests.request("PUT", f"{ppl_api_url}/lead/{parse.quote(event.get('pk'))}", data=json.dumps(body), headers=headers)

    event['payment_link'] = payment_link

    return event