from user import User
from db import init_db_command
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, jsonify, redirect, url_for, request, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView

from sqlalchemy import *
from flask_ngrok import run_with_ngrok
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

import sqlite3
import os
import requests
import random
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from dotenv import load_dotenv
load_dotenv()
import amqp_setup
import pika
import json

app = Flask(__name__)
from twitter import tweet
from firebase import Firebase
# run_with_ngrok(app)  # Start ngrok when app is run


basedir = os.path.abspath(os.path.dirname(__file__))

CORS(app, supports_credentials=True)

# Configs
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



## to call twitter service
# status = tweet("hello!")
# print(status)

######################################################################################
# Model layer
######################################################################################


######################################################################################
# AUTHENTICATION
######################################################################################

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
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


@app.route('/')  # should change to /manage
def index():
    if current_user.is_authenticated:  # determine if the current user interacting with app is logged in or not
        return jsonify({'pid': current_user.id, 'name': current_user.name, 'email': current_user.email, 'profile_pic': current_user.profile_pic}), 200
    else:
        message = json.dumps({ "Error" : "User not logged in", "Code" : 400 }) # python dict of error data -> json string
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="game.error", body=message) # publish to exchange
        print("not logged in")
        return "Bad request.", 400


def get_google_provider_cfg():  # retrieve Google's providor config.
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
    print("request_uri", request_uri)
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

        # publish user acc details to rabbitmq (activity)
        message = json.dumps( userinfo_response.json() ) # turn json object response into json string
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="game.activity", body=message)

    else:
        message = json.dumps({ "Error" : "User email not available or not verified by Google.", "Code" : 400 })
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="game.error", body=message)
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
    return redirect("https://127.0.0.1:8080/manageRoom")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out.", 200

######################################################################################
# ROOM CREATION (LOGIN REQUIRED)
######################################################################################

room_creation_params = {"profid": "", "questions": ""}


@app.route('/create', methods=['GET'])
@login_required #decorater (wrapper for function) deifined by flask-login. using google oauth, check if works. 
def createRoom():
    """
    Redirect to stripe payment page first
    Authenticated user  with all the details of the room/questions.
    """

    global room_creation_params

    # get POST body
    profid = request.args.get("pid")
    questions = request.args.get('q')

    # keep params for callback
    room_creation_params["profid"] = profid
    room_creation_params["questions"] = questions

    return redirect("http://127.0.0.1:5011/") # redirect to stripe payment confirmation page


@app.route('/create/callback')
@login_required
def createRoomCallback():
    """
    A unique RID is generated.
    Parse this json and send the room state to the database.
    Return a success message to the client.
    """
    request_data = {}

    # get GET params
    global room_creation_params
    pid = room_creation_params["profid"] # value: id integer
    q = room_creation_params["questions"] # value: list of question obj -> title, choices, dbsrc

    # business logic
    # print(pid)
    # print(json.loads(q))
    # translate data to format in model.py tables -> profid, questionid, roomid, question, choices -> qid and rid to be generated in Room.py
    # request_data = {"profid": "", "question X":{"":""}, } 
    request_data["profid"] = pid
    question_list = []
    for question_obj in json.loads(q):
        translated_qn = {} # create temp question object that stores formatted questions to be added to data to be requested
        translated_qn["question"] = question_obj["title"]
        translated_qn["choices"] = question_obj["choices"]
        question_list.append(translated_qn)
    
    request_data["questions"] = question_list
    print(request_data)
    # send request to Room.py with data to be mutated in graphql
    response = requests.post( "http://127.0.0.1:5004/create", data=json.dumps(request_data) ) 
    
    # print response code, get all rooms (to check + to log)

    # redirect to manageRoom
    print("redirecting to manageRoom now")
    return redirect("https://127.0.0.1:8080/manageRoom")   


@app.route('/getQuestionBank')
@login_required
def questionBank():
    """
    Authenticated user will request for question from the question bank.
    Retrieve the questions and return it as a json to the client.
    # """

    firebase_apikey = os.environ.get("firebase_apiKey")
    firebase_authDomain = os.environ.get("firebase_authDomain")
    firebase_databaseURL = os.environ.get("firebase_databaseURL")
    firebase_storageBucket = os.environ.get("firebase_storageBucket")
    firebase_appId = os.environ.get("firebase_appId")
    firebase_storageBucket = os.environ.get("firebase_storageBucket")
    
    config = {
        "apiKey": firebase_apikey,
        "authDomain": firebase_authDomain,
        "databaseURL": firebase_databaseURL,
        "storageBucket": firebase_storageBucket
    }

    try:

        # TO YASH:
        # There is an error here.

        firebase = Firebase(config)
        db = firebase.database()
        firebase_result = db.child("question").get()
        result = {}
        for data in firebase_result.each():
            result[data.key()] = data.val()
        return json.dumps(result), 200
    except Exception as e:
        print(f"Error: {e}")
        return "An error has occurred", 400



    
    # fb_app = firebase.FirebaseApplication('https://polarice-95e3e-default-rtdb.firebaseio.com/', None)
    # try: 
    #     result = jsonify(list(fb_app.get('/question', None).values()))
    #     return result, 200
    # except Exception as e:
    #     return e, 400
    

@app.route('/load')
@login_required
def start():
    """
    ----------------
    :Business Logic:
    ----------------
    Client calls this function, passing in the roomID (the PK of the rooms table)
    Authenticated user sends the roomID of the room to be started.
    The room will become live. A room that is not live cannot be connected by a student, even if the roomID exists.
    Create a Game Object in Game.py --> return questions and room code
    Store live rooms as a list within Game.py, with 7 digit room code
    A unique link is generated for clients to join via websocket
    Return the link to gameConsole to the authenticated client.

    This is just a simple function to make sure that the user is can only perform this when authenticated.
    """

    # start the room; make it live
    roomID = request.args.get('roomID')
    response = requests.post('http://127.0.0.1:5001/live', data={'roomID': roomID})
    roomCode = response.json()

    if response.status_code == 200:
        return f"/playGame/console/{roomCode}", 200

    return "Bad request", 400


if __name__ == '__main__':
    app.run(ssl_context="adhoc", host='0.0.0.0', port=5000)
    # app.run(ssl_context="adhoc", port=5000)
    # app.run(port=5000)
