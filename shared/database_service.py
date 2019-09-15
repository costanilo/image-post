import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def create_db_connection():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'image-post',
    })

    return firestore.client()


def get_data(collection):
    db = create_db_connection()
    users_ref = db.collection(collection)
    docs = users_ref.stream()


def create_data(collection, data):
    db = create_db_connection()
    ref = db.collection(collection).document()
    ref.set(data)


def get_all_used_quotes():
    with open('db.json', "r") as used_quotes:
        data = json.load(used_quotes)

    return data['used_quotes']


def set_new_quote(quote):
    with open('db.json', "r+") as used_quotes:
        data = json.load(used_quotes)
        data['used_quotes'].append(quote)
        used_quotes.seek(0)  # rewind
        json.dump(data, used_quotes, indent=2)
        used_quotes.truncate()


def get_font_configurations():
    with open('db.json', "r") as used_quotes:
        data = json.load(used_quotes)

    return data['font_configuration']


def get_font_configuration_by_name(font_name):
    with open('db.json', "r") as used_quotes:
        data = json.load(used_quotes)

    return [config for config in data['font_configuration'] if config['fontName']==font_name][0]


def set_used_image(url):
    with open('db.json', "r+") as used_quotes:
        data = json.load(used_quotes)
        data['used_images'].append(url)
        used_quotes.seek(0)  # rewind
        json.dump(data, used_quotes, indent=2)
        used_quotes.truncate()


def get_all_used_images():
    with open('db.json', "r") as used_quotes:
        data = json.load(used_quotes)
    return data['used_images']


def get_quotes_source():
    with open('db.json', "r") as used_quotes:
        data = json.load(used_quotes)

    return data['quotesSource']


def get_quotes_routes():
    with open('db.json', "r") as used_quotes:
        data = json.load(used_quotes)

    return data['quotesRoutes']
