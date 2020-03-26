__author__ = 'fernandocosta'

import requests, random, string
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

config = {
   'url' : 'https://gateway.marvel.com/v1/public/stories?apikey=',
   'public_key' : 'dc15e66b9ba195a9272d81d4a5ca4785',
   'private_key' : 'a469a57a45cef0b2a3404f5dda6f222c80c913fe',
   'base_url' : 'https://gateway.marvel.com/v1/public/'
} 

def full_hash():
   ts = str(datetime.utcnow().microsecond)
   return ts, (hashlib.md5(ts.encode('utf-8') + config['private_key'].encode('utf-8') + config['public_key'].encode('utf-8')).hexdigest())

def request_data(filter, description, element):
   ts, hash_data = full_hash()
   data = {
        'ts': ts, 
        'hash': hash_data, 
        'apikey': config['public_key'],
        'limit' : '10',
        filter : description #name 
   }

   comics = requests.get(config['base_url'] + element, params = data)
   return comics.content

@app.route("/")
def hello():
    return "Hello Quiver!!! e Equipe !!!"

# exemplo de chamada URL: http://localhost:5000/get_character?desc=Loki
@app.route("/get_character") 
def get_character():
    try:
        desc = request.args.get('desc')
        result = request_data('name', desc, 'characters')
        return result
    except Exception as e:
        return jsonify({'resultado': "OCORREU O SEGUINTE ERRO AO RESGATAR CHARACTER: " + str(e)})

# exemplo de chamada URL: http://localhost:5000/get_comics?desc=Loki
@app.route("/get_comics") 
def get_comics():
    try:
        desc = request.args.get('desc')
        result = request_data('title', desc, 'comics')
        return result
    except Exception as e:
        return jsonify({'resultado': "OCORREU O SEGUINTE ERRO AO RESGATAR COMICS: " + str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

