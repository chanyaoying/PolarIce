#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

# Processes all error log from various files and functions sent to activity queue via "*.error" key

import json
import os

import amqp_setup


import requests



tele_log_URL = "http://tele_log:5012/" # when sending get request to tele_log -> send logs to telegram group
monitorBindingKey='*.error'

def receiveError():
    amqp_setup.check_setup()
    
    queue_name = "Error"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error by " + __file__)
    processError(body)
    print() # print a new line feed

def processError(errorMsg):
    print("Printing the error message:")
    try:
        error = json.loads(errorMsg)
        # req_url = 'https://api.telegram.org/bot1569222163:AAG0_ajeXRNWghIyKQzkwDJ6HRjhKZBADRQ/sendMessage?chat_id=-1001315877981&text=' # "This is a test message"
        # req_url += errorMsg # adds json string message -> (error message content) to base url

        # requests.get(req_url)
        
        # pass python dict with error code to tele log function to send logs to tele bot
        # tele_log(error, "Error") 

        # requests.get(req_url)
        log_type = "Error"
        log_content = error
        # log_dict = {log_type : log_content} # dict to be passed on in request -> "Activity" : python dict
        response_obj = requests.get( f"{tele_log_URL}?log_type={log_type}&log_content={json.dumps(log_content)}" ) # tele_log/log_type/log_content
        # tele_log(order, "Activity")
        if response_obj.ok:
            print("successfully sent to tele bot") # successfully sent req and dispatched message to tele bot
            return response_obj.content, response_obj.status_code
        

        print("--JSON:", error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveError()
