import random
import sys

from google.cloud import firestore

db = firestore.Client()

MAX_RESOURCES = 3

# OPTIONS = {
#     'authDomain': "radlings.firebaseapp.com",
#     'databaseURL': "https://radlings.firebaseio.com",
#     'projectId': "radlings",
#     'storageBucket': "radlings.appspot.com",
#     'appId': "1:921916311052:web:a423832616acbb93bd5029"
# }


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
    try:
        categories = db.collection("categories").stream()

        categ_list = []

        for categ in categories:
            print(categ.id)
            categ_list.append(categ.id)

        return categ_list
    except Exception as e:
        print("Could not get categories".format(e), file=sys.stderr)
        return []


def add_resouce_to_db(rdata):
    try:
        category = rdata['category']
        tmp_json = {
            'title': rdata['title'],
            'description': rdata['description'],
            'source': rdata['source'],
            'url': rdata['url'],
            'helpful': 0,
            'not_helpful': 0,
            'impressions': 0,
            'discovery': 0
        }

        doc_ref = db.collection('all_resources').document(category).collection('resources').document()
        doc_ref.set(tmp_json)
        return 'Done'
    except Exception as e:
        print("Could not add resource {}".format(str(e)), file=sys.stderr)
        return 'Not Done'


def get_resource(categ):  # 3 resources
    try:
        resources = db.collection('all_resources').document(categ).collection('resources').stream()
        all_resources = []

        for res in resources:
            res_data = res.to_dict()
            tmp = {
                'title': res_data['title'],
                'description': res_data['description'],
                'source': res_data['source'],
                'url': res_data['url'],
                'helpful': res_data['helpful']
            }
            all_resources.append(tmp)

        sample_resources = random.sample(all_resources, min(MAX_RESOURCES, len(all_resources)))
        return sample_resources

    except Exception as e:
        print("Could not get three resources. {}".format(e), file=sys.stderr)
        return []


# --------- Flask Code begins --------- #

# !flask/bin/python
from flask import abort, Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/randquote')
def quote_route():
    try:
        response = get_random_quote()
        print(response)

        result = jsonify({
            'result': response,
            'success': True,
            'status': 'ok',
            'code': 200
        })

    except Exception as e:
        print("Could not get a random quote. {}".format(e), file=sys.stderr)

        result = jsonify({
            'result': {},
            'success': False,
            'status': str(e),
            'code': 500
        })

    result.headers.add('Access-Control-Allow-Origin', '*')
    return result


@app.route('/categories', methods=['GET'])
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


@app.route('/add_resource', methods=['POST'])
def add_resource_route():
    try:
        rdata = dict(request.get_json())
        response = add_resouce_to_db(rdata)

        result = jsonify({
            'result': response,
            'success': True,
            'status': 'ok',
            'code': 200
        })

    except Exception as e:
        print("Could not add a resource quote. {}".format(e), file=sys.stderr)
        result = jsonify({
            'result': None,
            'success': False,
            'status': str(e),
            'code': 500
        })

    result.headers.add('Access-Control-Allow-Origin', '*')
    return result


@app.route('/fetch_resource', methods=['GET'])
def fetch_resource_route():
    try:
        tmp = dict(request.args)
        categ = tmp['category']

        response = get_resource(categ)

        result = jsonify({
            'result': response,
            'success': True,
            'status': 'ok',
            'code': 200
        })

    except Exception as e:
        print("Could not fetch a resource quote. {}".format(e), file=sys.stderr)
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
