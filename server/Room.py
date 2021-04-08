from flask import Flask, request, jsonify, json
from flask_cors import CORS
import json
import requests

app = Flask(__name__)

CORS(app)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True


@app.route("/create", methods=['POST'])
def create_room():
    # mutate graph ql to create room
    data = request.data  # data to be mutated -> create room and questions
    # print("successfully reached /create")
    data_json = json.loads(data)
    print(data_json)

    # CREATE ROOM IN GRAPHQL
    # get rooms currently in gql table
    gql_rooms_response = requests.get(
        "http://127.0.0.1:5003/graphql?query=query{allRooms{edges{node{roomid profid}}}}")
    # gets json encoded response -> class : dict
    gql_rooms = gql_rooms_response.json()
    # print(gql_rooms)
    # + [num]["node"]["roomid"]/["profid"] for specific rooms
    print(gql_rooms["data"]["allRooms"]["edges"])

    # order list of room objects in ascending order
    rm_sorting_list = []  # temp list to store rooms
    for room_obj in gql_rooms["data"]["allRooms"]["edges"]:
        room_obj["node"]["roomid"] = int(room_obj["node"]["roomid"])
        # append actual room object (value of 'node' key)
        rm_sorting_list.append(room_obj["node"])

    # sorts list of room objects by roomid
    rm_sorted_list = sorted(rm_sorting_list, key=lambda i: i['roomid'])
    print(rm_sorted_list)

    # after ordering by roomid in asc order, retrieve the last roomid (largest) -> largest_rid = int
    # gets the int value of the last room object in sorted list
    largest_rid = int(rm_sorted_list[-1]["roomid"])
    print(largest_rid, type(largest_rid))

    # after retrieving largest roomid, create a new room id (+1 of largest roomid) and add into graphql table of rooms
    # room id generated based on largest roomid existing in rooms table
    roomid = str(largest_rid + 1)
    # prof id passed in from roomController as num str, divide by large number to make it fit as int
    profid = str(int(data_json["profid"]) / 1000000000000000)
    # profid = str(25)
    print(roomid, type(roomid), profid, type(profid),
          "will be created as a new room object in gql rooms table")
    room_post_url = 'http://127.0.0.1:5003/graphql?query=mutation{createRoom' + \
        f'(roomid:"{roomid}",profid:"{profid}")' + '{room{roomid profid}}}'
    room_mutation_response = requests.post(
        url=room_post_url)  # creates new room in gql table
    print(room_mutation_response.status_code)
    # bool for success of room mutation
    room_mutation_success = room_mutation_response.ok
    # print(requests.get( "http://127.0.0.1:5003/graphql?query=query{allRooms{edges{node{roomid profid}}}}" ).json()) # get all rooms to see

    # CREATE QUESTIONS IN GRAPHQL

    # get request to retrieve all questions in graphql tables -> request response
    # get json encoded response -> class : dict
    gql_questions_response = requests.get(
        "http://127.0.0.1:5003/graphql?query=query{allQuestions{edges{node{roomid questionid question choices}}}}")
    gql_questions = gql_questions_response.json()
    # print(gql_questions)

    # order list of question objects by question id in asc order
    qn_sorting_list = []  # temp list to store question objects to be sorted
    print(gql_questions["data"]["allQuestions"]["edges"])
    for qn_obj in gql_questions["data"]["allQuestions"]["edges"]:
        # convert to int to sort properly
        qn_obj["node"]["questionid"] = int(qn_obj["node"]["questionid"])
        # append actual question object (value of 'node' key)
        qn_sorting_list.append(qn_obj["node"])

    # order questions objects by questionid in asc order
    # sorts list of question objects by questionid
    qn_sorted_list = sorted(qn_sorting_list, key=lambda i: i['questionid'])
    print(qn_sorted_list)

    # after ordering by questionid in asc order, retrieve last qid in question list (largest) -> largest_qid = int
    largest_qid = qn_sorted_list[-1]["questionid"]
    print(largest_qid, type(largest_qid))

    # for each question in list of question objects received, generate a qid (+1 for each) and add into graphql of questions {roomid,questionid,question,choices}
    question_mutation_success = False
    for qn_obj in data_json["questions"]:

        questionid = str(largest_qid + 1)
        largest_qid += 1  # update largest qid for future loops
        question = qn_obj["question"]
        choices = qn_obj["choices"]
        question_post_url = 'http://127.0.0.1:5003/graphql?query=mutation{createQuestion' \
            + f'(roomid:"{roomid}",questionid:"{questionid}",question:"{question}",choices:"{choices}")' \
            + '{question{roomid questionid question choices}}}'

        question_mutation_response = requests.post(url=question_post_url)
        print(question_mutation_response.status_code,
              question_mutation_response.reason)
        question_mutation_success = question_mutation_response.ok

    # return response.ok if both requests have status code of <400
    # returns true only if new room is created and all passed questions are added
    return json.dumps(room_mutation_response.json())

@app.route("/rooms")
def get_rooms():
    # return all rooms in DB

    # get rooms currently in gql table
    # profid not needed since it's not restricted by prof anymore
    gql_rooms_response = requests.get(
        "http://127.0.0.1:5003/graphql?query=query{allRooms{edges{node{roomid}}}}")
    gql_rooms = gql_rooms_response.json()
    # + [num]["node"]["roomid"]/["profid"] for specific rooms
    # print(gql_rooms["data"]["allRooms"]["edges"])
    id_list = []  # list of room ids to be returned
    for room_obj in gql_rooms["data"]["allRooms"]["edges"]:
        room = room_obj["node"]  # actual room dict
        id_list.append(room["roomid"])  # adds each roomid in table to list

    # print(id_list)  # list of roomids in string format
    json_id_list = json.dumps(id_list)
    # print(json)

    return json_id_list, 200  # list of strings


@app.route("/roomQuestions/<roomid>")
def get_room_questions(roomid):
    # OBJECTIVE: get every question in graphql questions table with same profid value as passed -> [ {"title":"", "choices":"" } ]

    # get all question objects from questions table
    gql_questions_response = requests.get(
        "http://127.0.0.1:5003/graphql?query=query{allQuestions{edges{node{roomid questionid question choices}}}}")
    gql_questions = gql_questions_response.json()

    # iterate through question objects and add questions that match the roomid argument to list
    question_list = []
    print(roomid, type(roomid))
    for qn_obj in gql_questions["data"]["allQuestions"]["edges"]:
        question = qn_obj["node"]  # actual question dict
        print(question["roomid"], type(question["roomid"]))
        # both should be string type
        if question["roomid"].strip('"') == roomid.strip('"'):
            # format of question dict in returned list
            temp_dict = {
                "title": question["question"], "choices": question["choices"]}
            question_list.append(temp_dict)

    print(gql_questions)
    print(question_list)
    json_qn_list = json.dumps(question_list)
    return json_qn_list


if __name__ == '__main__':
    # app.run(port=<<<)
    # app.run(ssl_context="adhoc", host='0.0.0.0', port=5004)
    app.run(host='0.0.0.0', port=5004)
