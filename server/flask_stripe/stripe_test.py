from flask import Flask, render_template, url_for, request, abort, jsonify, redirect, json
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()
import stripe

app = Flask(__name__)
CORS(app)
app.config['ENV'] = 'development'
app.config['DEBUG'] = False



stripe_keys = {
    "secret_key": os.environ.get("STRIPE_SECRET_KEY"),
    "publishable_key": os.environ.get("STRIPE_PUBLISHABLE_KEY"),
}

stripe.api_key = stripe_keys["secret_key"]
print(stripe_keys)

# app.config['STRIPE_PUBLIC_KEY'] = 'YOUR_STRIPE_PUBLIC_KEY'
# app.config['STRIPE_SECRET_KEY'] = 'YOUR_STRIPE_SECRET_KEY'
# stripe.api_key = app.config['STRIPE_SECRET_KEY']


"""
# Placeholder Page, same as page with 'Create Room' button
"""
@app.route('/')
def index():
    '''
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1GtKWtIdX0gthvYPm4fJgrOr',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    '''
    return render_template(
        'index.html', 
        #checkout_session_id=session['id'], 
        #checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1IZFzZAbp1R4NDVpmK7hwGgS',
            'quantity': 1,
        }],
        mode='payment',
        # success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        success_url = 'https://127.0.0.1:5000/create/callback', # proceed with room creation on successful payment
        cancel_url='https://127.0.0.1:8080/manageRoom', # redirect back to room management page if cancelled or payment failure
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': stripe_keys["publishable_key"]
    }

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

if __name__ == "__main__":
    app.run(port=5011)