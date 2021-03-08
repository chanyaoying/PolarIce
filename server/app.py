from flask import Flask, render_template, request, json, jsonify
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

app = Flask(__name__)

# Internal imports
from db import init_db_command
from user import User

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

CORS(app)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

socketio = SocketIO(app, cors_allowed_origins="*")

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
    print('Running...')
    socketio.run(app)