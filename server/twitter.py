import tweepy
from tweepy import OAuthHandler
import os
from flask import Flask, request, jsonify, json
import json


app = Flask(__name__)

#App Configuration
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

# Authentication
consumer_key = os.environ.get("twitter_consumer_key", None)
consumer_secret = os.environ.get("twitter_consumer_secret", None)
access_token = os.environ.get("twitter_access_token", None)
access_secret = os.environ.get("twitter_access_secret", None)

# The following two lines create an authorization object with your above authentication info.
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Sends a tweet to the Polarice Twitter account of the Room code and Pin so that players can see
@app.route("/<roomCode>")
def tweet(roomCode):
    tweet = f"A room with PIN:{roomCode} is now live. Feel free to join if you FOMO" # tweet to be sent

    # This line finally calls Twitter's Rest API.
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.update_status(tweet)
    except tweepy.TweepError as error:
        return (error.response.text, 400)
    return "Success", 200

# tweet("Test Tweet")


if __name__ == '__main__':
    app.run(port=5013, host="0.0.0.0")