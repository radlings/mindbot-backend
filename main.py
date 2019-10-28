import random

from config import firebase_config

def get_db():
    import pyrebase

    config = firebase_config

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return db

def get_random_quote():
    MAX_NUMBER = 10
    t = random.randint(1, MAX_NUMBER)
    print(t)

    db = get_db()
    quotes = db.child('quotes').get().val()

    cont = 1
    for k, v in quotes.items():
        if cont == t:
            return v
        cont += 1

    return None


# --------- Flask Code begin --------- #

#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/randquote')
def solve():
    response = get_random_quote()
    print(response)
    return jsonify({
        'result': response,
        'status': 'ok',
        'code': 200
    })


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]