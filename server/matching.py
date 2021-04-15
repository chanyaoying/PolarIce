from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import scipy.spatial
import pandas as pd
from datetime import datetime

app = Flask(__name__)


app.config['ENV'] = 'development'
app.config['DEBUG'] = True

####
# Routes
####


@app.route("/match", methods=['GET'])
def matching():
    result = json.loads(request.args.get('results'))

    # player names
    user_data = list(result.keys())

    # all users choices
    user_choices = list(result.values())

    # placeholder columns
    columns = ["nonesense" * len(list(result.values()))]

    df_choices = pd.DataFrame(user_choices, columns=columns,
                              index=user_data)

    jaccard = scipy.spatial.distance.cdist(df_choices, df_choices,
                                           metric='jaccard')

    user_distance = pd.DataFrame(jaccard, columns=user_data,
                                 index=user_data)

    # prepare a dictionary
    user_rankings = {}

    # iterate over the columns in the dataframe
    for user in user_distance.columns:

        # extract the distances of the column ranked by smallest
        distance = user_distance[user].nsmallest(len(user_distance))

        # for each user, create a key in the dictionary and assign a
        # list that contains a ranking of its most similar users
        data = {user: [i for i in distance.index if i != user]}
        user_rankings.update(data)

    return jsonify(user_rankings), 200


if __name__ == '__main__':
    app.run(port=5005, host="0.0.0.0")
