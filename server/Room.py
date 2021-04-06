from flask import Flask, request, jsonify, json
from flask_cors import CORS
import json
import requests

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

@app.route("/create", methods=['POST'])
def create_room():
    # mutate graph ql to create room
    data = request.data # data to be mutated -> create room and questions
    # print("successfully reached /create")
    # print(json.loads(data))

    # create room in graphql
    gql_rooms = requests.get( "http://127.0.0.1:5003/graphql?query=query{allRooms{edges{node{roomid profid}}}}" ) # get rooms currently in gql table 
    gql_rooms = gql_rooms.json() # gets json encoded response -> class : dict
    print(gql_rooms)
    print(gql_rooms["data"]["allRooms"]["edges"]) # + [num]["node"]["roomid"]/["profid"] for specific rooms
    # create questions in graphql


    
    return {}


@app.route("/rooms")
def get_rooms():
    # return all rooms in DB
    pass


if __name__ == '__main__':
    app.run(port=5004)