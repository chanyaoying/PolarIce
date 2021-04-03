from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import scipy.spatial
import pandas as pd  
from datetime import datetime

app = Flask(__name__)


app.config['ENV'] = 'development'
app.config['DEBUG'] = True

#users name 
user_data = ["User A", "User B", "User C", "User D", "User E", "User F"]

#all users choices 
user_choices = [[1,1,0,0],
                [1,1,1,0], 
                [1,0,0,0],
                [1,0,1,1],
                [0,0,1,1],
                [0,1,1,1]]

df_choices = pd.DataFrame(user_choices, columns=['Apples', 
                          'Bananas', 'Pineapples', 'Kiwis'], 
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
    data = {user : [i for i in distance.index if i!=user]}
    user_rankings.update(data)

print(user_rankings)

####
# Routes
####

@app.route("/matching", methods=['POST'])
def matching():
    #result = request.json.get('result', None)
    result_list = result.items()

    return (result_list)
   
if __name__ == '__main__':
    app.run(port=5002)