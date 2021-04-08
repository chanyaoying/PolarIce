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
    global cache
    for roomCode, players in cache["live_data"].items():
        if sid in players:
            return roomCode
    return False


####
# Cache (to improve networking speeds)
####

# TODO
# rebuild cache on startup
# build with data from Game.py

# live_data: list of players in the game
# current_question: current question number in the game
# started: whether the live game has started or not
# questions_list: the list of questions
cache = {"live_data": {'testRoom': {'testSid1': "TestPlayer1", 'testSid2': "TestPlayer2"}},
         "current_question": {'testRoom': 0}, "started": {'testRoom': False}, "questions_list": {'testRoom': {}}, "counts": {"testRoom": 0}, "results": {"testRoom": []}}

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
        code = requests.get(
            f"http://127.0.0.1:5002/getGame/{roomID}").status_code
        return jsonify({'live': code == 200}), 200

    if request.method == 'POST':

        try:
            roomID = request.form['roomID']
        except Exception as error:
            print(error)  # for logging
            raise error

        # create game instance in Game.py, making the game live
        # questions as well as the room code should be returned
        response = requests.post(
            "http://127.0.0.1:5002/create", data={'roomID': roomID}).json()
        code = response['code']
        questions = response['questions']

        # initiate caching
        cache["live_data"][code] = {}
        cache["current_question"][code] = 0
        cache["started"][code] = False
        cache["questions_list"][code] = questions
        cache["results"][code] = {}
        cache["counts"][code] = 0

        return jsonify(response['code']), 200

    return "Bad request.", 400


@app.route("/match/<roomCode>")
def match(roomCode):
    """
    Carries out the business logic for matching.
    1. Gets the cached results by roomCode
    2. Put it into the Game object for data translation. Translated data will be returned.
    3. Invoke the Matching microservice. A list of matchings will be returned.
    """
    results = json.dumps(cache["results"][roomCode])

    
    
    # invoke Game.py
    transformed_result = requests.get(f"http://127.0.0.1:5002/match/{roomCode}", params={"results": results}).json()

    print("##############################################################3")
    print(transformed_result)

    # invoke Matching.py
    response = requests.get("http://127.0.0.1:5005/match", params={"results": results})
    if response.status_code == 200:

        # cache results
        cache["results"][roomCode] = response.json()

        return "Matching successful.", 200
    else:
        return "Matching failed.", 400

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

    if roomCode in cache["live_data"]:  # if room is live

        join_room(roomCode)
        print(f"{username} joined {roomCode}.")

        # bypass adding prof in player list
        if not gameMaster:
            cache['live_data'][roomCode][request.sid] = username
            print(list(cache['live_data'][roomCode].values()),
                  ", added " + username)
            emit('join', {"roomID": roomCode,
                          "message": f"{username} has entered the room."}, room=roomCode)

        # get current list of players
        emit('receivePlayers', cache['live_data'][roomCode], room=roomCode)

        # get current question number if user rejoins halfway and the game has ended
        emit('nextQuestion', cache["current_question"]
             [roomCode], room=roomCode)

        # get cached question_list
        emit('getQuestions', cache["questions_list"][roomCode], room=roomCode)

        # show gameArea if the game has started
        component = "gameArea" if cache["started"][roomCode] else "gameLobby"
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
    if request.sid in cache['live_data'][roomCode]:
        cache['live_data'][roomCode].pop(request.sid)
    else:
        print(f"player: {username} is not in the room.")

    print(f"players: {cache['live_data'][roomCode]}; removed {username}")
    emit("leave", {"roomID": roomCode,
                   "message": f"{username} has left the room."}, room=roomCode)
    emit('receivePlayers', cache['live_data'][roomCode], room=roomCode)


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

    if roomCode and request.sid in cache['live_data'][roomCode]:
        username = cache['live_data'][roomCode][request.sid]
        cache['live_data'][roomCode].pop(request.sid)
        print(f"Removed {request.sid} from all rooms.")
        emit('disconnect', {
             "roomID": roomCode, "message": f"{username} has disconnected."}, room=roomCode)
        emit('receivePlayers', cache['live_data'][roomCode], room=roomCode)
    else:
        print(f"player: {request.sid} is not in the room.")


####
# Messaging Events
####

@socketio.on('getCurrentPlayers')
def on_getCurrentPlayers(data):
    print("trying to get all players now")
    roomCode = data['roomID']
    emit('receivePlayers', cache['live_data'][roomCode], room=roomCode)


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


# as prof clicks "Start", change component to "gameArea", which already displays the first question
@socketio.on('startGame')
def on_startGame(data):
    roomCode = data['roomID']
    # set game status to true when the game starts
    cache["started"][roomCode] = True

    # Add players into the Game object
    players_to_add = json.dumps(list(cache['live_data'][roomCode].values()))
    print(players_to_add)
    response = requests.get(
        f"http://127.0.0.1:5002/addPlayers/{roomCode}", params={"players": players_to_add})
    if response.status_code == 400:
        print("Unable to add players in Game object.")

    print(f"Starting game at {roomCode}.")
    emit("changeComponent", "gameArea", room=roomCode)
    emit("nextQuestion", 0, room=roomCode)


@socketio.on('endGame')
def on_endGame(data):
    roomCode = data['roomID']
    cache["current_question"][roomCode] = 0
    cache["started"][roomCode] = False
    print(f"Ending game at {roomCode}.")
    emit("changeComponent", "gameLobby", room=roomCode)
    emit("nextQuestion", 0, room=roomCode)
    

@socketio.on("collectAnswers")
def on_collectAnswers(data):
    roomCode = data['roomID']
    emit("endGame", True, room=roomCode)



@socketio.on('nextQuestion')
def on_nextQuestion(data):
    roomCode = data['roomID']
    currentQuestionNumber = data['currentQuestionNumber']

    nextQuestionNumber = (currentQuestionNumber +
                          1) % (len(cache["questions_list"][roomCode]) + 1)

    cache["current_question"][roomCode] = nextQuestionNumber

    print(f"Next question number: {nextQuestionNumber} at {roomCode}.")
    emit("nextQuestion", nextQuestionNumber, room=roomCode)


@socketio.on('getQuestions')
def on_getQuestions(data):
    roomCode = data['roomID']
    questions = cache["current_question"][roomCode]
    print(f"Getting questions for {request.sid} at {roomCode}.")
    emit("getQuestions", questions, room=roomCode)


@socketio.on('sendResult')
def on_sendResult(data):
    """
    Each player's responses are collected here.
    """
    roomCode = data['roomID']
    nickname = data['nickname']
    results = data['results']

    # cache the results
    cache["results"][roomCode][nickname] = results

    # add to counts; track how many has submitted
    cache['counts'][roomCode] += 1
    current = cache['counts'][roomCode]
    total = len(cache["live_data"][roomCode])
    print({"current": current, "total": total})
    emit("submissionCount", {"current": current, "total": total}, room=roomCode)


@socketio.on('getMatching')
def on_getMatching(data):
    """
    This function is called by the prof when the matching is successful.
    Changes UI component and resets question displayed (if played again).
    """
    print("$$$$$$$$$$$$$$$$$$$$$$$$$4\ngetMatching called")
    roomCode = data['roomID']
    emit("getMatching", True, room=roomCode)
    emit("nextQuestion", 0, room=roomCode)
    emit("changeComponent", "matchResults", room=roomCode) # change to matching component on frontend #TODO


@socketio.on("matchingResult")
def on_matchingResult(data):
    """
    Each client invokes this function to get their personalized matching.
    """
    roomCode = data['roomID']
    nickname = data["nickname"]

    personal_room = str(roomCode) + nickname
    join_room(personal_room)

    results = cache['results'][roomCode]
    personalized_result = results.get(nickname, False)

    if personalized_result and len(personalized_result) > 3:
        personalized_result = personalized_result[:3]

    emit("matchingResult", personalized_result, room=personal_room)



if __name__ == '__main__':
    socketio.run(app, port=5001)
