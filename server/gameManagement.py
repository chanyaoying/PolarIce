# gameManagement is an orchestrator that:
# 1. Manages game state as the game is being played
# 2. Create websocket connections between clients and the server
# 3. Receive messages from the clients, which changes the game state
# 4. Update the clients on the game state


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from invokes import invoke_http

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
    global players_data
    for room, players in players_data.items():
        if sid in players:
            return room
    return False


####
# Data
####

players_data = {'testRoom': {'testSid1': "TestPlayer1",
                             'testSid2': "TestPlayer2"}}  # placeholder

questions_data = {'testRoom': {'started': False,'currentQuestionNumber': 0, 'questions': [{
    "title": 'Are you a cat or dog person?',
    "choices": ['Cat', 'Dog']
},
    {
        "title": 'Are you a happy or sad person?',
        "choices": ['Happy', 'Sad']
},
    {
        "title": 'Are you a female or male person?',
        "choices": ['Female', 'Male']
},
    {
        "title": 'Are you a introvert or extrovert person?',
        "choices": ['Introvert', 'Extrovert']
},
    {
        "title": 'Are you a tall or short person?',
        "choices": ['Tall', 'Short']
},
    {
        "title": 'I think carefully before I say something.?',
        "choices": ['YES', 'NO']
},
    {
        "title": 'I’m a “Type A” go-getter. I’d rather die than quit.',
        "choices": ['YES', 'NO']
},
    {
        "title": 'I feel overwhelmed and I’m not sure what to change.',
        "choices": ['YES', 'NO']
},
    {
        "title": 'I make decisions based on logic.',
        "choices": ['YES', 'NO']
},
    {
        "title": 'I appreciate it when someone gives me their undivided attention.',
        "choices": ['YES', 'NO']
},
]}}


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
            print(error)  # for logging
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

    try:
        gameMaster = data['gameMaster']
    except:
        gameMaster = False

    if room in players_data:  # if room is live

        join_room(room)
        print(f"{username} joined {room}.")

        # bypass adding prof in player list
        if not gameMaster:
            players_data[room][request.sid] = username
            print(players_data[room], "added " + username)
            emit('join', {"roomID": room,
                          "message": f"{username} has entered the room."}, room=room)

        emit('receivePlayers', players_data[room], room=room) # get current players data
        emit('nextQuestion', questions_data[room] 
             ['currentQuestionNumber'], room=room) # get current question number if user rejoins halfway and the game has ended
        component = "gameArea" if questions_data[room]['started'] else "gameLobby"
        emit('changeComponent', component, room=room) # get game status if when user joins (user can join a started game)
        # get questions data
        # emit("getQuestions", "test", room=room)

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
    if request.sid in players_data[room]:
        players_data[room].pop(request.sid)
    else:
        print(f"player: {username} is not in the room.")
    print(players_data[room], "removed " + username)
    emit("leave", {"roomID": room,
                   "message": f"{username} has left the room."}, room=room)
    emit('receivePlayers', players_data[room], room=room)


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
    emit('connect', f'User {request.sid} connected', broadcast=True)


@socketio.on('disconnect')
def test_connect():
    print("Client disconnected.")
    global num_users
    num_users -= 1

    room = getRoomOfUser(request.sid)

    if room and request.sid in players_data[room]:
        username = players_data[room][request.sid]
        players_data[room].pop(request.sid)
        print(f"Removed {request.sid} from all rooms.")
        emit('disconnect', {
             "roomID": room, "message": f"{username} has disconnected."}, room=room)
        emit('receivePlayers', players_data[room], room=room)
    else:
        print(f"player: {request.sid} is not in the room.")


####
# Messaging Events
####

@socketio.on('getCurrentPlayers')
def on_getCurrentPlayers(data):
    print("trying to get all players now")
    room = data['roomID']
    emit('receivePlayers', players_data[room], room=room)


@socketio.on('sendMessage')
def handle_sendMessage(data):
    print('message received: ', data)
    msg = data['msg']
    username = data['nickname']
    room = data['roomID']
    emit('receiveMessage', {"roomID": room,
                            "message": f"{username}: {msg}"}, room=room)


####
# Game Events
####

# as users join, send questions data to them
@socketio.on('loadGame')
def on_loadGame(data):
    room = data['roomID']
    print(f"sending game data of {room} to user {request.sid}")
    # send question data from here


# as prof clicks "Start", change component to "gameArea", which already displays the first question
@socketio.on('startGame')
def on_startGame(data):
    room = data['roomID']
    questions_data[room]['started'] = True
    print(f"Starting game at {room}.")
    emit("changeComponent", "gameArea", room=room)


@socketio.on('endGame')
def on_endGame(data):
    room = data['roomID']
    questions_data[room]["currentQuestionNumber"] = 0
    questions_data[room]['started'] = False
    print(f"Ending game at {room}.")
    emit("changeComponent", "gameLobby", room=room)


@socketio.on('nextQuestion')
def on_nextQuestion(data):
    room = data['roomID']
    currentQuestionNumber = data['currentQuestionNumber']

    nextQuestionNumber = (currentQuestionNumber +
                          1) % (len(questions_data[room]['questions']) + 1)

    print(f"Next question number: {nextQuestionNumber} at {room}.")
    emit("nextQuestion", nextQuestionNumber, room=room)


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
