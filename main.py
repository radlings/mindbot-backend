import firebase_admin
from firebase_admin import db
from firebase_admin import firestore
# from firebase_admin import credentials
import random


options = {
    'authDomain': "radlings.firebaseapp.com",
    'databaseURL': "https://radlings.firebaseio.com",
    'projectId': "radlings",
    'storageBucket': "radlings.appspot.com",
    'appId': "1:921916311052:web:a423832616acbb93bd5029"
}

# This must only be called once.
app = firebase_admin.initialize_app(options=options)


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

    quotes = db.reference('quotes').get()

    cont = 1
    for k, v in quotes.items():
        if cont == t:
            return v
        cont += 1

    return None


# --------- Flask Code begins --------- #

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