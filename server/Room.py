from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

@app.route("/create")
def create_room():
    # mutate graph ql to create room
    pass


@app.route("/rooms")
def get_rooms():
    # return all rooms in DB
    pass


if __name__ == '__main__':
    app.run(port=5004)