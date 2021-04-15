from telegram import *
from telegram.ext import *
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, json
import json


app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = False

# Sends content of log message (python dictionary) to telegram bot

# prepare to set up link to tele bot
token = os.environ.get("tele_bot_token")
print('tele_bot_token' in os.environ)
print(token)
bot = Bot(token) # link to tele bot using bot token

# live chat_id = -441770919 ESD GROUP CHAT ID
# chat_id = -1001315877981  TEST BOT GROUP CHAT ID 
chat_id = "-1001315877981" # link to the group to send message to (bot must be inside group with access to messages)

@app.route("/") # when port 5012 is accessed -> log activity/ error message
def tele_log(): 

    log_type = request.args.get('log_type')
    log_content = json.loads(request.args.get('log_content')) # gets python object (dict) of logs content e.g. { "key" : "value" }
    
    # send message to tele in a formatted manner -> line by line
    # iterate through every key-value pair in dict
    # log_content = json.loads(log_content_json)
    test_str = f"<b><u>Logging : {log_type}</u></b>\n\n"
    for key, value in log_content.items():
        test_str += f"<u>{key}</u> : {value}\n" 

    # dispatch message to tele bot
    bot.sendMessage( chat_id, test_str, parse_mode="HTML" )



if __name__ == '__main__':
    app.run(port=5012, host="0.0.0.0")