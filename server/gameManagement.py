# gameManagement is an orchestrator that:
# 1. Manages game state as the game is being played
# 2. Create websocket connections between clients and the server
# 3. Receive messages from the clients, which changes the game state
# 4. Update the clients on the game state


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

socketio = SocketIO(app, cors_allowed_origins="*")



####
# Data
####

players_data = {'testRoom': ['TestPlayer1', 'TestPlayer2']} # placeholder


####
# Room creation Event
####

@app.route('/live', methods=['GET', 'POST'])
def startRoom(): 
    """
    Get room data from graphql model or from roomManagement.py (not decided yet)
    
    GET: Return all live rooms.
    POST: Put the roomID into live_rooms, return that live room.
    """
    
    global players_data

    if request.method == 'GET':
        roomID = request.args.get('roomID')
        return jsonify({'live': roomID in players_data}), 200
    
    if request.method == 'POST':
        try:
            roomID = request.form['roomID']
        except Exception as error:
            print(error) # for logging
            raise error
            
        players_data[roomID] = []
        
        # for logging
        print(f"Room with roomID: {roomID}")
        
        return jsonify(players_data[roomID]), 200

    return "Bad request.", 400
    
        


####
# Room join/leave Events
####

@socketio.on('join')
def on_join(data):
    global players_data
    username = data['username']
    room = data['roomID']

    if room in players_data: # if room is live
        join_room(room)
        players_data[room].append(username)
        print(players_data[room], "added " + username)
        emit('join', f"{username} has entered the room.", room=room)
    else:
        # return error
        # send message which includes error
        pass

@socketio.on('leave')
def on_leave(data):
    global players_data
    username = data['username']
    room = data['roomID']
    leave_room(room)
    players_data[room].remove(username)
    print(players_data[room], "removed " + username)
    emit("leave", username + ' has left the room.', room=room)



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



####
# Messaging Events
####

@socketio.on('getCurrentPlayers')
def on_getCurrentPlayers(data):
    room = data['roomID']
    emit('receivePlayers', players_data[room], room=room)

@socketio.on('sendMessage')
def handle_sendMessage(data):
    print('message received: ', data)
    msg = data['msg']
    username = data['nickname']
    room = data['roomID']
    emit('receiveMessage', f"{username}: {msg}", room=room)



if __name__ == '__main__':
    socketio.run(app, port=5001)






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



