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
import markdown  # Import the markdown library

app = Flask(__name__)
CORS(app)  # Optional


def get_top_questions(tag="python"):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "votes",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": 5,
        "filter": "withbody"  # Use the 'withbody' filter to include the question body
    }
    response = requests.get(url, params=params)
    questions = response.json().get("items", [])
    return questions

def get_top_answer(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",  # Sort answers by votes
        "site": "stackoverflow",
        "filter": "withbody"  # Include the body of the answers
    }
    response = requests.get(url, params=params)
    answers = response.json().get("items", [])
    return answers[0]['body'] if answers else "No answers available"

@app.route("/questions")
def questions():
    tag = request.args.get("tag", "python")  # Default to 'python' if no tag is provided
    index = request.args.get("index", 0)  # Default to the first question (index 0)
    questions = get_top_questions(tag)
    
    index = int(index)
    if 0 <= index < len(questions):
        question = questions[index]
        question['body'] = markdown.markdown(question.get('body', ''))
        # Fetch the most voted answer instead of the accepted answer
        question['answer'] = markdown.markdown(get_top_answer(question['question_id']))
    else:
        # If the index is invalid, return the first question by default
        question = questions[0]
        question['body'] = markdown.markdown(question.get('body', ''))
        question['answer'] = markdown.markdown(get_top_answer(question['question_id']))

    return render_template("questions.html", question=question, questions=questions, tag=tag, index=index + 1)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080)
    app.run(debug=True, port=os.getenv("PORT", default=5000))
