from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/testpoint')
def test():
    return "Server Alive"


@socketio.on('connect')
def test_connect():
    print("User connected.")
    # keep track of how many active connections there are as a failsafe
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
    socketio.run(port=5001)
