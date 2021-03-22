from telegram import *
import requests


# Sends content of log message (python dictionary) to telegram bot

def tele_log(json_obj_content, log_type_str): # gets python object (dict) of logs content e.g. { "key" : "value" }

    # prepare to set up link to tele bot
    bot = Bot("1569222163:AAG0_ajeXRNWghIyKQzkwDJ6HRjhKZBADRQ") # link to tele bot using bot token

    # live chat_id = -441770919 ESD GROUP CHAT ID
    # chat_id = -1001315877981  TEST BOT GROUP CHAT ID 
    chat_id = "-1001315877981" # link to the group to send message to (bot must be inside group with access to messages) 

    # send message to tele in a formatted manner -> line by line
    # iterate through every key-value pair in dict
    test_str = f"<b><u>Logging : {log_type_str}</u></b>\n\n"
    for key, value in json_obj_content.items():
        test_str += f"<u>{key}</u> : {value}\n" 

    # dispatch message to tele bot
    bot.sendMessage( chat_id, test_str, parse_mode="HTML" )