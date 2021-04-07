# Handles the Game object based on inputs from gameManagement
# the game object is mutated here
# This microservice can be used for any Quiz-type game

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from random import randint

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

####
# Game Object
####

Games = {0: 0}


class Game:

    def __init__(self, roomID, questions):
        self.roomID = roomID
        self.timeCreated = datetime.now().strftime("%a, %d/%m/%Y %H:%M:%S")

        # dict: {sid: username, ...}
        self.players = []

        # {qid: {"title": "..." ,"choice": "..."}, ...}
        self.questions = questions

        self.results = {}

        self.code = 0

    def __repr__(self):
        return f"Game object for roomID: {self.roomID}, created at {self.timeCreated}"

    def setResult(self, results, filler=None):

        # data translation
        transformed = {}
        for nickname, answer in results.items():
            for i in range(len(self.questions)):
                if str(i) not in answer.keys():
                    answer[str(i)] = filler
            transformed[nickname] = answer

        transformed = {nickname: answers.values()
                       for nickname, answers in transformed.items()}

        # add missing players
        for player in self.players:
            if player not in transformed:
                transformed[player] = [filler * qNo]

        self.result = transformed

    def getResult(self):
        return json.dumps(self.results)

    def addPlayers(self, players):
        # add new players to the game even if it has started
        self.players.extend(players)
        return jsonify([self.roomID, self.players, self.questions])

    def getCode(self):
        """
        Have to register the Game object inside Games, or else the code won't be persistent.
        """
        global Games
        while (self.code in Games):
            self.code = str(randint(1000000, 9999999))
        return self.code

####
# Routes
####


@app.route("/create", methods=["POST"])
def createGame():
    """
    Instantiate the Game object and put it in Games dict.
    Gets the question from the database.
    Returns the questions if successful.
    """

    roomID = request.form['roomID']
    players = json.loads(request.form['players'])

    # TODO
    # query from GQL
    questions = [{"title": "Are you a cat or dog person?",
                  "choices": "True/False"}, {"title": "Yes or no?", "choices": "Yes/No"}, {"title": "Are you okay?", "choices": "Not okay./Meh."}]  # placeholder

    # instantiate Game object
    newGame = Game(roomID, questions)
    gameCode = newGame.getCode()
    Games[gameCode] = newGame

    print(f"Game created. Game code: {gameCode}")
    print(f"Games now: {Games}")

    return jsonify({'questions': newGame.questions, 'code': gameCode}), 200


@app.route('/getGame/<roomCode>')
def getGame(roomCode):
    roomCode = str(roomCode)
    try:
        GameInstance = Games[roomCode]
    except KeyError as err:
        GameInstance = False
    return (repr(GameInstance), 200) if GameInstance else ("Game not instantiated.", 400)


@app.route("/addPlayers/<roomCode>")
def addPlayers(roomCode):
    """
    Params:
    - roomCode <int>: the identifier

    GET:
    players (json): list of new players
    """
    global Games

    targetGame = Games.get(roomCode, False)

    if targetGame:
        players = json.loads(request.args.get('players'))
        # get players who are not in the Game object
        newPlayers = [
            player for player in players if player not in targetGame.players]
        targetGame.addPlayers(newPlayers)
        print(targetGame.players)
        return "Players added.", 200
    return "Game not found.", 400


@app.route("/match/<roomCode>")
def match(roomCode):
    """
    Params:
    - roomCode <int>: the identifier

    GET:
    results  (json): list of new players
    """
    global Games

    targetGame = Games.get(roomCode, False)

    if targetGame:

        # dict: each key is a player nickname and each value is a dict: {index, answer}
        results = json.loads(request.args.get('results'))

        targetGame.setResult(results, filler=None)

        return jsonify(targetGame.getResult()), 200

    return "Game instance not found.", 400


if __name__ == '__main__':
    print(Games)
    app.run(port=5002)
