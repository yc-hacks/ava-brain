from flask import Flask, request

from qa import Ava

# EB looks for an 'application' callable by default.
application = Flask(__name__)

ava = Ava()

@application.route('/')
def hello():
    print(request)
    return 'Hello World'

@application.route('/ask', methods = ['GET', 'POST'])
def ask():
    print(request)
    return ava.ask("When was Princeton founded?")

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host="0.0.0.0", port=80)
