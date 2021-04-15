#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

# Processes all activity log from various files and functions sent to activity queue due to "#" key

import json
import os

import amqp_setup
import requests
from flask import jsonify


tele_log_URL = "http://tele_log:5012/" # when sending get request to tele_log -> send logs to telegram group
monitorBindingKey='*.activity'

def receiveActivityLog():
    amqp_setup.check_setup()
        
    queue_name = 'Activity_Log'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an event log by " + __file__)
    processOrderLog(body)
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an order log:")
    print(order) # prints log in terminal/console

    activity_content = json.loads(order)
    # requests.get(req_url)
    log_type = "Activity"
    log_content = activity_content
    # response_obj = requests.get( f"{tele_log_URL}{log_type}/{json.dumps(log_content)}" ) # tele_log/log_type/log_content
    response_obj = requests.get( f"{tele_log_URL}?log_type={log_type}&log_content={json.dumps(log_content)}" ) 
    # tele_log(order, "Activity")
    if response_obj.ok:
        print("successfully sent to tele bot") # successfully sent req and dispatched message to tele bot
        return response_obj.content, response_obj.status_code

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveActivityLog()
