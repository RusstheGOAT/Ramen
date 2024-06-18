from flask import Flask, render_template, jsonify, request, url_for
import json
import random
from datetime import datetime

app = Flask(__name__)

# load
def load_ramen_shops():
    with open('ramen_shops.json', 'r', encoding='utf-8') as file:
        return json.load(file)

ramen_shops = load_ramen_shops()

with open("data.json", "r", encoding="utf-8") as data_file:
    data = json.load(data_file)

with open("finalAnswers.json", "r", encoding="utf-8") as answer_file:
    finalAnswers = json.load(answer_file)

currentQuiz = None

@app.route('/')
def index():
    global currentQuiz
    currentQuiz = None
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

@app.route('/quiz')
def quiz():
    global currentQuiz
    currentQuiz = 0
    currentQuestion = data[currentQuiz]["question"]
    options = ""
    for idx, option in enumerate(data[currentQuiz]["answers"]):
        options += f"<input name='options' type='radio' value='{idx}'><label>{option[0]}</label><br><br>"
    return render_template("quiz.html", question=currentQuestion, options=options, buttonText="下一題", show_home_button=False)

@app.route("/submit", methods=["POST"])
def submit():
    global currentQuiz
    if request.method == "POST":
        if currentQuiz is None:
            currentQuiz = 0
            currentQuestion = data[currentQuiz]["question"]
            options = ""
            for idx, option in enumerate(data[currentQuiz]["answers"]):
                options += f"<input name='options' type='radio' value='{idx}'><label>{option[0]}</label><br><br>"
            return render_template("quiz.html", question=currentQuestion, options=options, buttonText="下一題", show_home_button=False)
        else:
            user_answer = request.form["options"]
            next_step = data[currentQuiz]["answers"][int(user_answer)][1]
            if isinstance(next_step, int):
                currentQuiz = next_step - 1
                currentQuestion = data[currentQuiz]["question"]
                options = ""
                for idx, option in enumerate(data[currentQuiz]["answers"]):
                    options += f"<input name='options' type='radio' value='{idx}'><label>{option[0]}</label><br><br>"
                return render_template("quiz.html", question=currentQuestion, options=options, buttonText="下一題", show_home_button=False)
            else:
                finalAnswer = finalAnswers[next_step]
                finalAnswerContent = f"""
                <h3>{finalAnswer['店名']}</h3>
                <p>店家地址: {finalAnswer['店家地址']}</p>
                <p>聯絡電話: {finalAnswer['聯絡電話']}</p>
                <p>營業時間:</p>
                <ul>
                """
                for time in finalAnswer['營業時間']:
                    finalAnswerContent += f"<li>{time}</li>"
                finalAnswerContent += "</ul>"
                finalAnswerImage = url_for('static', filename=finalAnswer["image"])
                finalAnswerContent += f"<br><br><img src='{finalAnswerImage}' alt='{finalAnswer['店名']}' style='max-width: 600px; max-height: 600px; object-fit: cover;'><br><br>"
                currentQuiz = None
                return render_template("quiz.html", question=finalAnswer['店名'], options=finalAnswerContent, buttonText="重新作答", show_home_button=True)
    return render_template("quiz.html", show_home_button=True)

if __name__ == '__main__':
    app.run(debug=True)
