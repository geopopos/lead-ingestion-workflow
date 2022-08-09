import stripe, os, requests, json

from urllib import parse

stripe_api_key = os.environ.get('STRIPE_API_KEY')
ppl_api_url ="https://e6b1hc9rfg.execute-api.us-east-1.amazonaws.com"

if os.environ.get('IS_LOCAL') == 'true':
    stripe_api_key = os.environ.get('STRIPE_TEST_API_KEY')
    ppl_api_url = "http://localhost:2000"

if os.environ.get('STAGE') == 'dev':
    stripe_api_key = os.environ.get('STRIPE_TEST_API_KEY')

def create_lead_product_stripe(event, context):
    stripe.api_key = stripe_api_key
    lead_id = event.get('pk')
    product = stripe.Product.create(
        name=f"Lead-{lead_id}",
        metadata={"lead_id": lead_id}
    )

    product_id = product.id

    body = {
        "product_id": product_id,
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("PUT", f"{ppl_api_url}/lead/{parse.quote(lead_id)}", data=json.dumps(body), headers=headers)
    event['product'] = product
    return event 