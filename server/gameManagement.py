# gameManagement is an orchestrator that:
# 1. Manages game state as the game is being played
# 2. Create websocket connections between clients and the server
# 3. Receive messages from the clients, which changes the game state
# 4. Update the clients on the game state


from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

socketio = SocketIO(app, cors_allowed_origins="*")



####
# Room join/leave Events
####

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)



####
# Connection Events
####

# reset number of users when server restarts
num_users = 0

@socketio.on('connect')
def test_connect():
    print("Client connected.")
    global num_users
    num_users += 1
    emit('connect', num_users, broadcast=True)


@socketio.on('disconnect')
def test_connect():
    print("Client disconnected.")
    global num_users
    num_users -= 1
    emit('disconnect', num_users, broadcast=True)


@socketio.on('sendMessage')
def handle_sendMessage(data):
    print('message received: ', data)
    msg = data['msg']
    roomID = data['roomID']
    emit('receiveMessage', msg, broadcast=True)



if __name__ == '__main__':
    socketio.run(app, port=5001)



####
# Connection Events
####





# @socketio.on('message')
# def handle_message(msg):
#     print('received message: ' + str(msg))
#     send(str(msg), broadcast=True)


# @socketio.on("my event")
# def handle_custom_event(data):
#     print(f"Custom event data: {data}")
#     print(f"Custom event type: {type(data)}")


# @socketio.on('testing')
# def testing(msg):
#     print(msg)
#     emit('testing', "This message came from the server")

# @socketio.on('join')
# def on_join(join_arg):
#     print(f'Room joined. join_arg: {join_arg}')



