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

authors = deta.Base("authors_for_quotes")   
auths_usernames = list(map(lambda c:c.screen_name,api.get_friends(screen_name="makeittshirt",count=200)))

for username in auths_usernames:
	if authors.fetch({"screen_name":username}).count != 0:
		break
	req = requests.get(os.environ.get("DETA_URLL")+f'{username}')
	try:
		data = req.json()
		if data['error']: 
			continue
		key = 1_000_000_000 - data['followers_count']
		key = str(key).zfill(9)
		if authors.fetch({"key":key}).count != 0:
			num = 0
			while authors.fetch({"key":key+ str(num)}).count != 0:
				num += 1
			authors.put({"key":key+str(num),"profile_image":data['profile_image'],"name":data['name'],"screen_name":username,"verified":data['verified']})
			continue
		authors.put({"key":key,"profile_image":data['profile_image'],"name":data['name'],"screen_name":username,"verified":data['verified']})
	except:
		continue

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
