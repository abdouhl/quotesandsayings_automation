from os.path import join, dirname
from dotenv import load_dotenv
import os
from supabase import create_client, Client
import requests

load_dotenv(join(dirname(__file__), '.env'))


supabase: Client = create_client(os.environ.get("SUPABASE_URL"),os.environ.get("SUPABASE_KEY"))

authors = []
for num in range(0,10):
    authors.extend(supabase.table("authors").select('*').range(num*1000,num*1000+1000).execute().data)

for author in authors:
    print(author['screen_name'])
    req = requests.get(os.environ.get("DETA_URLL")+author['screen_name'])
    try:
        data =req.json()
        supabase.table("authors").update({'followers_count': data['followers_count'], 'profile_image': data['profile_image'], 'name': data['name']}).eq("key", author['key']).execute()
    except:
        continue
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
