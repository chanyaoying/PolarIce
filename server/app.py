from flask import Flask, render_template, request, json, jsonify, redirect, url_for, session
from dotenv import load_dotenv
load_dotenv()

# from flask.ext.session import Session
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from oauthlib.oauth2 import WebApplicationClient
import random
import requests
import os
import sqlite3
# Internal imports
from db import init_db_command
from user import User

app = Flask(__name__)

CORS(app)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

socketio = SocketIO(app, cors_allowed_origins="*")

######################################################################################

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
print("CLIENT ID IS", GOOGLE_CLIENT_ID)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)   
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# root route should display ENTER ROOM ID + MANAGE ROOMS
@app.route('/') # should change to /manage
def index():
    if current_user.is_authenticated: #determine if the current user interacting with app is logged in or not
        # return (
        #     "<p>Hello, {}! You're logged in! Email: {}</p>"
        #     "<div><p>Google Profile Picture:</p>"
        #     '<img src="{}" alt="Google profile pic"></img></div>'
        #     '<a class="button" href="/logout">Logout</a>'.format(
        #         current_user.name, current_user.email, current_user.profile_pic
        #     )
        # )
        session['auth'] = current_user
        print("auth session", session['auth'])
        print('hello world')
        redirect("https://localhost:8080/allRoom")
        return jsonify({'code': 200, 'name':current_user.name, 'email': current_user.email, 'profile_pic': current_user.profile_pic})
    else:
        return jsonify({'code': 400})

def get_google_provider_cfg(): # retrieve Google's providor config. 
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    print("request_uri",request_uri)
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # either (cookie) jwt/access token? 
    # session['auth'] = unique_id
    return redirect("https://localhost:8080/allRoom/"+ unique_id) #send to create room

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

######################################################################################

@app.route('/testpoint')
def test():
    return "Server Alive"

# @app.route("/testconsole")
# def testconsole():
#     return render_template("index.html")

@socketio.on('connect')
def test_connect():
    print("User connected.")
    emit('connect', "User connected.")

# @socketio.on('disconnect')
# def test_connect():
#     print("Client disconnected.")

@socketio.on('message')
def handle_message(msg):
    print('received message: ' + str(msg))
    send(str(msg), broadcast=True)

@socketio.on("my event")
def handle_custom_event(data):
    print(f"Custom event data: {data}")
    print(f"Custom event type: {type(data)}")

@socketio.on('testing')
def testing(msg):
    print(msg)
    emit('testing', "This message came from the server")

# @socketio.on('create')
# def on_create(arg):
#     room = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_LENGTH))
#     print(f'Room created. ID: {room}\nArg: {arg}')

# @socketio.on('join')
# def on_join(join_arg):
#     print(f'Room joined. join_arg: {join_arg}')




if __name__ == '__main__':
    # print('Running...')
    # socketio.run(app)
    app.run(ssl_context="adhoc")