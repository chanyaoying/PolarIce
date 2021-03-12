# Imports 
from user import User
from db import init_db_command
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, jsonify, redirect, url_for, request, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
# from schema import schema
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

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# app.add_url_rule('/graphql', view_func=GraphQLView.as_view( #add graphQL
#     'graphql',
#     schema=schema,
#     graphiql=True,
# ))

CORS(app, supports_credentials=True)

# Configs
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)

######################################################################################
# Models
######################################################################################
class Room(db.Model):
    __tablename__ = 'rooms'
    
    roomid = db.Column(db.Integer, primary_key=True)
    profid = db.Column(db.Integer, index=True, unique=True)
    # questions = db.relationship('Question', backref='author')
    
    def __repr__(self):
        return '< %r>' % self.profid
# class Question(db.Model):
#     __tablename__ = 'questions'
    
#     questionid = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String(256), index=True)
#     # answer = db.Column(db.Text) # not sure about this     
#     prof_id = db.Column(db.Integer, db.ForeignKey('rooms.profid')) # not sure about this
    
    # def __repr__(self):
    #     return '<Question %r>' % self.question

# Schema Objects 
''' 
show what kind of type of object will be shown in the graph. 
'''

class RoomObject(SQLAlchemyObjectType):
    class Meta:
        model = Room
        interfaces = (graphene.relay.Node, )
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_roooms = SQLAlchemyConnectionField(RoomObject)
    # all_users = SQLAlchemyConnectionField(UserObject)
schema = graphene.Schema(query=Query)

class CreateRoom(graphene.Mutation):
    class Arguments:
        roomid = graphene.Int(required=True)
        profid = graphene.Int(required=True) 

    room = graphene.Field(lambda: RoomObject)

    def mutate(self, info, roomid, profid):
        room = Room(roomid=roomid, profid=profid)
        # if room is not None:
        #     post.author = user
        db.session.add(room)
        db.session.commit()
        return CreateRoom(room=room)
class Mutation(graphene.ObjectType):
    create_room = CreateRoom.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)

# Routes 
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)


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
        return jsonify({'name': current_user.name, 'email': current_user.email, 'profile_pic': current_user.profile_pic}), 200
    else:
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
    return redirect("https://127.0.0.1:8080/allRoom")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

######################################################################################
# ROOM CREATION (LOGIN REQUIRED)
######################################################################################

# TODO


@app.route('/create')
@login_required #decorater (wrapper for function) deifined by flask-login. using google oauth, check if works. 
def createRoom():
    """
    Authenticated user  with all the details of the room/questions.
    A unique RoomID is generated.
    Parse this json and send the room state to the database.
    Return a success message to the client.
    """
    pass


@app.route('/getQuestionBank')
@login_required
def questionBank():
    """
    Authenticated user will request for question from the question bank.
    Retrieve the questions and return it as a json to the client.
    """
    pass


@app.route('/start/<int:roomID>')
@login_required
def start(roomID):
    """
    Authenticated user sends the roomID of the room to be started.
    Invoke the gameManagment microservice.
    The gameManagment microservice should return a unique link to join the game.
    Return the unique link to the client.
    """
    pass


if __name__ == '__main__':
    app.run(ssl_context="adhoc", port=5000)
