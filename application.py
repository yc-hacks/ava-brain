import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from qa import Ava

# EB looks for an 'application' callable by default.
application = Flask(__name__)
CORS(application)

ava = Ava()

podcastDF = pd.read_csv('./data/podcasts/podcasts.csv', names=["uuid", 'title', 'author', 'description', 'category', 'image'])

@application.route('/')
def hello():
    print(request)
    return 'Hello World'


@application.route('/ask', methods = ['GET', 'POST'])
@cross_origin()
def ask():
    question = request.args.get('question')
    answers = ava.ask(question)
    uuid = answers['data']['uuid']

    
    podcastData = podcastDF.loc[podcastDF['uuid'] == uuid].iloc[0]

    response = jsonify({
        "success": True,
        'shortAnswer': answers['answer'],
        'longAnswer': answers['paragraph'],
        'episode': {
            'title': answers['title'],
            'summary': answers['data']['summary'],
            'link': answers['data']['link'],
            'uuid': answers['data']['uuid'],
        },
        'podcast': {
            'title': podcastData['title'],
            'author': podcastData['author'],
            'category': podcastData['category'],
            'image': podcastData['image'],
            'description': podcastData['description']
        }
    })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host="0.0.0.0", port=80)
