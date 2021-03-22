import tweepy
from tweepy import OAuthHandler
import os

def tweet(tweet):

    consumer_key = os.environ.get("twitter_consumer_key", None)
    consumer_secret = os.environ.get("twitter_consumer_secret", None)
    access_token = os.environ.get("twitter_access_token", None)
    access_secret = os.environ.get("twitter_access_secret", None)

    # The following two lines create an authorization object with your above authentication info.
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # This line finally calls Twitter's Rest API.
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.update_status(tweet)
    except tweepy.TweepError as error:
        return (error, 400)
    return "Success", 200
