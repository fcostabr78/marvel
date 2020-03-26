import requests, random, string
import hashlib
from datetime import datetime

config = {
   'url' : 'https://gateway.marvel.com/v1/public/stories?apikey=',
   'public_key' : 'dc15e66b9ba195a9272d81d4a5ca4785',
   'private_key' : 'a469a57a45cef0b2a3404f5dda6f222c80c913fe',
   'base_url' : 'https://gateway.marvel.com/v1/public/'
} 

def full_hash():
   ts = str(datetime.utcnow().microsecond)
   return ts, (hashlib.md5(ts.encode('utf-8') + config['private_key'].encode('utf-8') + config['public_key'].encode('utf-8')).hexdigest())

def request_data(character):
   ts, hash_data = full_hash()
   data = {
        'ts': ts, 
        'hash': hash_data, 
        'apikey': config['public_key'],
        'title' : character
   }

   comics = requests.get(config['base_url']+'comics', params = data)
   print(comics.content)

def get_character(name):
   request_data(name)
   return name

character = input('\nDigite o nome de um personagem q deseja localizar: ')
print("Localizar o personagem => {}".format(get_character(character)))

