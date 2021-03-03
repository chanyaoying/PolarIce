from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
import random
from settings import ID_LENGTH

app = Flask(__name__)
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


# @socketio.on('connect')
# def test_connect():
#     print("User connected.")


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