from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime

app = Flask(__name__)

def load_ramen_shops():
    with open('ramen_shops.json', 'r', encoding='utf-8') as file:
        return json.load(file)

ramen_shops = load_ramen_shops()

@app.route('/')
def index():
    cities = list(set(shop['city'] for shop in ramen_shops))
    return render_template('index.html', cities=cities)

@app.route('/random_ramen', methods=['POST'])
def random_ramen():
    data = request.get_json()
    city = data.get('city')
    if city == '都可以':
        filtered_shops = ramen_shops
    else:
        filtered_shops = [shop for shop in ramen_shops if shop['city'] == city]
    
    if filtered_shops:
        selected_shop = random.choice(filtered_shops)
        return jsonify(selected_shop)
    else:
        return jsonify({'error': 'No ramen shops found in the selected city'})

@app.route('/current_time')
def current_time():
    now = datetime.now()
    return jsonify({'current_time': now.strftime("%Y-%m-%d %H:%M:%S")})

@app.route('/ramen_game')
def ramen_game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
