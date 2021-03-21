# Handles the Game object based on inputs from gameManagement
# the game object is mutated here

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

####
# Game Object
####

Games = {}

class Game:

    def __init__(self, roomID, players, questions):
        self.roomID = roomID

        # dict: {sid: username, ...}
        self.players = players

        # {qid: {"title": "..." ,"choice": "..."}, ...}
        self.questions = questions

        self.currentQuestion = 0
        self.results = {}

    def answerQuestion(self, sid, qid):
        # gameManagement will call on a route to update the Game object
        pass

    def getResult(self):
        # translate the result into json to pass to the Matching Microservice
        return self.results

    def testMethod(self):
        return "It's working."

####
# Routes
####


@app.route("/create", methods=["POST"])
def createGame():
    """
    Instantiate the Game object and put it in Games dict.
    Gets the question from the database.
    Gets
    """
    print(request.method)

    roomID = request.form['roomID']
    players = json.loads(request.form['players'])

    # query from GQL
    question_query_result = {"1": {"title": "Are you a cat or dog person?","choice": "True/False"}, "2": {"title": "Yes or no?", "choice": "Yes/No"}} # placeholder
    
    # split choices by "/"
    questions = {qid: {"title": q["title"], "choice": q['choice'].split("/")} for qid, q in question_query_result.items()}
    
    # prevent memory leak
    del question_query_result

    #instantiate Game object
    newGame = Game(roomID, players, questions)

    global Games
    Games[roomID] = newGame

    return f"Successfully created game at room: {roomID}", 200

@app.route('/')
def index():
    GameInstance = Games.get('testRoom', False)
    return GameInstance.testMethod() if GameInstance else "Does not work."

if __name__ == '__main__':
    app.run(port=5002)