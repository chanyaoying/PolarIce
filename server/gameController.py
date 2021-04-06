# gameManagement is an orchestrator that:
# 1. Manages game state as the game is being played
# 2. Create websocket connections between clients and the server
# 3. Receive messages from the clients, which changes the game state
# 4. Update the clients on the game state


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import json
import requests

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

socketio = SocketIO(app, cors_allowed_origins="*")


####
# Helper functions
####


def getRoomOfUser(sid):
    global live_data
    for roomCode, players in live_data.items():
        if sid in players:
            return roomCode
    return False


####
# Cache (to improve networking speeds)
####

# list of players in the game
live_data = {'testRoom': {'testSid1': "TestPlayer1",
                             'testSid2': "TestPlayer2"}}

# current question number in the game
questions_data = {'testRoom': 0}

# whether the live game has started or not
started = {'testRoom': False}

####
# Room creation Event
####

@app.route('/live', methods=['GET', 'POST'])
def startRoom():
    """
    Get room data from graphql model or from roomManagement.py (not decided yet)

    GET: Check if a room is live
    POST: Put the code into live_data, return that live room.
    """

    # Check if a room is live
    if request.method == 'GET':
        roomID = request.args.get('roomID')
        code = requests.get(f"http://127.0.0.1:5002/getGame/{roomID}").status_code
        return jsonify({'live': code == 200}), 200

    if request.method == 'POST':

        try:
            roomID = request.form['roomID']
            # placeholder
            players = json.dumps(["testPlayer3", "testPlayer4"]) # get current players in the room before the game has started
        except Exception as error:
            print(error)  # for logging
            raise error

        # create game instance in Game.py, making the game live
        # questions as well as the room code should be returned
        response = requests.post("http://127.0.0.1:5002/create", data={'roomID': roomID, 'players': players}).json()
        code = response['code']

        # initiate caching
        live_data[code] = {}
        questions_data[code] = 0
        started[code] = False

        return jsonify(response), 200

    return "Bad request.", 400


####
# Room join/leave Events
####

@socketio.on('join')
def on_join(data):
    global live_data
    username = data['username']
    roomCode = data['roomID']

    try:
        gameMaster = data['gameMaster']
    except:
        gameMaster = False

    if roomCode in live_data:  # if room is live

        join_room(roomCode)
        print(f"{username} joined {roomCode}.")

        # bypass adding prof in player list
        if not gameMaster:
            live_data[roomCode][request.sid] = username
            print(list(live_data[roomCode].values()), ", added " + username)
            emit('join', {"roomID": roomCode,
                          "message": f"{username} has entered the room."}, room=roomCode)

        # get current list of players
        emit('receivePlayers', live_data[roomCode], room=roomCode)
        
        # get current question number if user rejoins halfway and the game has ended
        emit('nextQuestion', questions_data[roomCode], room=roomCode)

        # show gameArea if the game has started
        component = "gameArea" if started[roomCode] else "gameLobby"
        emit('changeComponent', component, room=roomCode)

    else:
        # return error
        # send message which includes error
        pass


@socketio.on('leave')
def on_leave(data):
    
    username = data['username']
    roomCode = data['roomID']
    leave_room(roomCode)
    if request.sid in live_data[roomCode]:
        live_data[roomCode].pop(request.sid)
    else:
        print(f"player: {username} is not in the room.")

    print(f"players: {live_data[roomCode]}; removed {username}")
    emit("leave", {"roomID": roomCode,
                   "message": f"{username} has left the room."}, room=roomCode)
    emit('receivePlayers', live_data[roomCode], room=roomCode)


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
    print(f'User {request.sid} connected. Current players={num_users}')
    emit('connect', f'User {request.sid} connected', broadcast=True)


@socketio.on('disconnect')
def test_connect():
    print("Client disconnected.")
    global num_users, live_data
    num_users -= 1

    roomCode = getRoomOfUser(request.sid)

    if roomCode and request.sid in live_data[roomCode]:
        username = live_data[roomCode][request.sid]
        live_data[roomCode].pop(request.sid)
        print(f"Removed {request.sid} from all rooms.")
        emit('disconnect', {
             "roomID": roomCode, "message": f"{username} has disconnected."}, room=roomCode)
        emit('receivePlayers', live_data[roomCode], room=roomCode)
    else:
        print(f"player: {request.sid} is not in the room.")


####
# Messaging Events
####

@socketio.on('getCurrentPlayers')
def on_getCurrentPlayers(data):
    print("trying to get all players now")
    roomCode = data['roomID']
    emit('receivePlayers', live_data[roomCode], room=roomCode)


@socketio.on('sendMessage')
def handle_sendMessage(data):
    print('message received: ', data)
    msg = data['msg']
    username = data['nickname']
    roomCode = data['roomID']
    emit('receiveMessage', {"roomID": roomCode,
                            "message": f"{username}: {msg}"}, room=roomCode)


####
# Game Events
####

# MIGHT NOT BE USED; PLEASE CHECK
# as users join, send questions data to them
# @socketio.on('loadGame')
# def on_loadGame(data):
#     roomCode = data['roomID']
#     print(f"sending game data of {roomCode} to user {request.sid}")
#     # send question data from here
#     # TODO


# as prof clicks "Start", change component to "gameArea", which already displays the first question
@socketio.on('startGame')
def on_startGame(data):
    roomCode = data['roomID']
    started[roomCode] = True # set game status to true when the game starts

    # Add players into the Game object
    # TODO

    print(f"Starting game at {roomCode}.")
    emit("changeComponent", "gameArea", room=roomCode)
    emit("nextQuestion", 0, room=roomCode)


@socketio.on('endGame')
def on_endGame(data):
    roomCode = data['roomID']
    questions_data[roomCode] = 0
    started[roomCode] = False
    print(f"Ending game at {roomCode}.")
    emit("changeComponent", "gameLobby", room=roomCode)
    emit("nextQuestion", 0, room=roomCode)


@socketio.on('nextQuestion')
def on_nextQuestion(data):
    roomCode = data['roomID']
    currentQuestionNumber = data['currentQuestionNumber']

    nextQuestionNumber = (currentQuestionNumber +
                          1) % (len(questions_data[roomCode]) + 1)

    questions_data[roomCode] = nextQuestionNumber

    print(f"Next question number: {nextQuestionNumber} at {roomCode}.")
    emit("nextQuestion", nextQuestionNumber, room=roomCode)


@socketio.on('getQuestions')
def on_getQuestions(data):
    roomCode = data['roomID']
    questions = questions_data[roomCode]
    print(f"Getting questions for {request.sid} at {roomCode}.")
    emit("getQuestions", questions, room=roomCode)


if __name__ == '__main__':
    socketio.run(app, port=5001)
