import tweepy
from os.path import join, dirname
from dotenv import load_dotenv
import os
from supabase import create_client, Client
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

supabase: Client = create_client(os.environ.get("SUPABASE_URL"),os.environ.get("SUPABASE_KEY"))

likes_ids = api.get_favorites(count=200).ids()
for num in range(0,10):
    likes_ids.extend(api.get_favorites(count=200,max_id=min(likes_ids)).ids())

likes_ids= list(set(likes_ids))

for like_id in likes_ids:
	print(like_id)
	if supabase.table("quotes").select('*').eq('tweet_id',str(like_id)).execute().data != []:
		continue
	try:
		tweett_url = os.environ.get("A_URLL")+ f"{like_id}"
		tweett = requests.get(tweett_url).json()
	except:
		print("error")
		continue
	lang = tweett['lang']
	first = tweett['display_text_range'][0]
	last = tweett['display_text_range'][1]
	text = tweett['text'][first:last]
	username = tweett['user']['screen_name'] 
	auth_data = supabase.table("authors").select('*').eq('screen_name',username).execute().data
	if auth_data == []:
		req = requests.get(os.environ.get("DETA_URLL")+username)
		try:
			data =req.json()
		except:
			print("error1")
			continue
		supabase.table("authors").insert({'followers_count': data['followers_count'], 'profile_image': data['profile_image'], 'name': data['name'], 'screen_name': username, 'en': lang == 'en', 'es': lang == 'es', 'fr': lang == 'fr', 'pt': lang == 'pt', 'de': lang == 'de', 'ar': lang == 'ar'}).execute()
	elif not auth_data[0][lang]:
		req = requests.get(os.environ.get("DETA_URLL")+username)
		try:
			data =req.json()
		except:
			print("error2")
			continue
		supabase.table("authors").update({'followers_count': data['followers_count'], 'profile_image': data['profile_image'], 'name': data['name'], 'screen_name': username, 'en': lang == 'en' or auth_data[0]["en"], 'es': lang == 'es' or auth_data[0]["es"], 'fr': lang == 'fr' or auth_data[0]["fr"], 'pt': lang == 'pt' or auth_data[0]["pt"], 'de': lang == 'de' or auth_data[0]["de"], 'ar': lang == 'ar' or auth_data[0]["ar"]}).eq("key", auth_data[0]["key"]).execute()
	supabase.table("quotes").insert({'lang': lang, 'text': text, 'tweet_id': str(like_id), 'username': username}).execute()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
