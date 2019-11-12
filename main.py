import random
import logging

from google.cloud import firestore

db = firestore.Client()

FORMAT = "[*] %(asctime)15s - [%(levelname)s] - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# OPTIONS = {
#     'authDomain': "radlings.firebaseapp.com",
#     'databaseURL': "https://radlings.firebaseio.com",
#     'projectId': "radlings",
#     'storageBucket': "radlings.appspot.com",
#     'appId': "1:921916311052:web:a423832616acbb93bd5029"
# }

# This must only be called once.

"""Get a random quote from Firebase Realtime Database
Run ``gcloud auth application-default login`` in your shell first! 
This will store application default credentials on your local machine.

https://firebase.google.com/docs/admin/setup/
"""


def get_random_quote():
    # We may need this for GAE deployment. Leave this for now.
    # app_default = credentials.ApplicationDefault()
    # app_default_credential = app_default.get_credential()

    MAX_NUMBER = 10
    t = random.randint(1, MAX_NUMBER)
    print(t)

    quotes_docs = db.collection(u"quotes").stream()

    cont = 1
    for quote in quotes_docs:
        if cont == t:
            return quote.to_dict()
        cont += 1

    return None


def get_category_list():
    categories = db.collection("categories").stream()

    categ_list = []

    for categ in categories:
        print(categ.id)
        categ_list.append(categ.id)

    return categ_list

def add_resouce_to_db():
    return None


# --------- Flask Code begins --------- #

# !flask/bin/python
from flask import abort, Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/randquote')
def quote_route():
    try:
        response = get_random_quote()
        logging.info(response)

        result = jsonify({
            'result': response,
            'success': True,
            'status': 'ok',
            'code': 200
        })

    except Exception as e:
        logging.exception("Could not get a random quote.")

        result = jsonify({
            'result': {},
            'success': False,
            'status': str(e),
            'code': 500
        })

    result.headers.add('Access-Control-Allow-Origin', '*')
    return result


@app.route('/categories', methods = ['GET'])
def category_route():
    try:
        response = get_category_list()
        result = jsonify({
            'result': response,
            'success': True,
            'status': 'ok',
            'code': 200
        })

    except Exception as e:
        result = jsonify({
            'result': None,
            'success': False,
            'status': str(e),
            'code': 500
        })

    result.headers.add('Access-Control-Allow-Origin', '*')
    return result


@app.route('/add_resource', methods = ['POST'])
def add_resource_route():
    try:
        response = add_resouce_to_db()
        result = jsonify({
            'result': response,
            'success': True,
            'status': 'ok',
            'code': 200
        })

    except Exception as e:
        result = jsonify({
            'result': None,
            'success': False,
            'status': str(e),
            'code': 500
        })

    result.headers.add('Access-Control-Allow-Origin', '*')
    return result


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
