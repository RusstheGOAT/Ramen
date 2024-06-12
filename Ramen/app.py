from flask import Flask, render_template, jsonify
import requests
import json
import random
from datetime import datetime

app = Flask(__name__)

API_KEY = 'YOUR_GOOGLE_API_KEY'  # 替換為您的Google API金鑰
PLACE_DETAILS_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
PLACE_INFO_URL = 'https://maps.googleapis.com/maps/api/place/details/json'

def load_ramen_shops():
    with open('ramen_shops.json', 'r', encoding='utf-8') as file:
        return json.load(file)

ramen_shops = load_ramen_shops()

def get_place_details(name, city):
    params = {
        'input': f'{name}, {city}',
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': API_KEY
    }
    response = requests.get(PLACE_DETAILS_URL, params=params)
    if response.status_code == 200:
        results = response.json().get('candidates', [])
        if results:
            place_id = results[0]['place_id']
            return get_place_info(place_id)
    return None

def get_place_info(place_id):
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,opening_hours,price_level',
        'key': API_KEY
    }
    response = requests.get(PLACE_INFO_URL, params=params)
    if response.status_code == 200:
        result = response.json().get('result', {})
        return {
            'name': result.get('name'),
            'address': result.get('formatted_address'),
            'hours': result.get('opening_hours', {}).get('weekday_text', 'N/A'),
            'price_range': result.get('price_level', 'N/A')
        }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_ramen')
def random_ramen():
    shop = random.choice(ramen_shops)
    details = get_place_details(shop['name'], shop['city'])
    if details:
        return jsonify(details)
    else:
        return jsonify(shop)  # 直接返回JSON文件中的資料

@app.route('/current_time')
def current_time():
    now = datetime.now()
    return jsonify({'current_time': now.strftime("%Y-%m-%d %H:%M:%S")})

if __name__ == '__main__':
    app.run(debug=True)
