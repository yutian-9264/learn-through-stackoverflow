# from flask import Flask, jsonify
import os

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


# if __name__ == '__main__':
#     app.run(debug=True, port=os.getenv("PORT", default=5000))



from flask import Flask, jsonify, request, render_template
from flask_cors import CORS  # Optional if not calling externally
import requests

app = Flask(__name__)
CORS(app)  # Optional


def get_top_questions(tag="python"):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "votes",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": 10,
        "filter": "!9_bDDxJY5"
    }
    response = requests.get(url, params=params)
    questions = response.json().get("items", [])
    return questions

def get_top_answer(answer_id):
    url = f"https://api.stackexchange.com/2.3/answers/{answer_id}"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody"
    }
    response = requests.get(url, params=params)
    answers = response.json().get("items", [])
    return answers[0]['body'] if answers else None

@app.route("/questions")
def questions():
    tag = request.args.get("tag", "python")
    questions = get_top_questions(tag)
    for q in questions:
        if 'accepted_answer_id' in q:
            q['answer'] = get_top_answer(q['accepted_answer_id'])
        else:
            q['answer'] = "No accepted answer"
    return jsonify(questions)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080)
    app.run(debug=True, port=os.getenv("PORT", default=5000))
