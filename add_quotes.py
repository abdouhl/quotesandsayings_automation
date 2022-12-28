import tweepy
from os.path import join, dirname
from dotenv import load_dotenv
import os
from deta import Deta
import requests


load_dotenv(join(dirname(__file__), '.env'))

twitter_auth_keys = {
	"consumer_key"        : os.environ.get("A_BOT_CONSUMER_KEY"),
	"consumer_secret"     : os.environ.get("A_BOT_CONSUMER_SECRET"),
	"access_token"        : os.environ.get("A_BOT_ACCESS_TOKEN"),
	"access_token_secret" : os.environ.get("A_BOT_ACCESS_TOKEN_SECRET")
}

auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
        )
auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
        )
api = tweepy.API(auth)

deta = Deta(os.environ.get("DETA_KEY"))
quotes = deta.Base("quotes")

likes_ids = api.get_favorites(count=200).ids()

for like_id in likes_ids:
    if quotes.fetch({"tweet_id":like_id}).count != 0:
        continue
    try:
        tweett_url = os.environ.get("A_URLL")+ f"{like_id}"
        tweett = requests.get(tweett_url).json()
    except:
        continue
    lang = tweett['lang']
    first = tweett['display_text_range'][0]
    last = tweett['display_text_range'][1]
    text = tweett['text'][first:last]
    username = tweett['user']['screen_name'] 
    key = 1_000_000_000 - tweett['favorite_count']
    key = str(key).zfill(9)
    if quotes.fetch({"key":key}).count != 0:
        num = 0
        while quotes.fetch({"key":key+ str(num)}).count != 0:
            num += 1
        quotes.put({"key":key+str(num),"lang":lang,"tweet_id":like_id,"username":username,"text":text})
        continue
    quotes.put({"key":key,"lang":lang,"tweet_id":like_id,"username":username,"text":text})

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
