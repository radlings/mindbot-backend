import random

from config import firebase_config

def get_db():
    import pyrebase

    config = firebase_config

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return db

def getQuote():
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
    return "Hello, World!"

@app.route('/getQuote')
def solve():
    response = getQuote()
    print(response)
    return jsonify({
        'result': response,
        'status': 'ok',
        'code': 200
    })


if __name__ == '__main__':
    app.run(debug = True)