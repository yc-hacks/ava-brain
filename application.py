from flask import Flask, request
from flask_cors import CORS

from qa import Ava

# EB looks for an 'application' callable by default.
application = Flask(__name__)
CORS(application)

ava = Ava()

@application.route('/')
def hello():
    print(request)
    return 'Hello World'


@application.route('/ask', methods = ['GET', 'POST'])
def ask():
    question = request.args.get('question')
    answers = ava.ask(question)
    response = flask.jsonify({
        "success": True,
        'shortAnswer': answers['answer'],
        'title': answers['title'],
        'longAnswer': answers['paragraph']
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host="0.0.0.0", port=80)
