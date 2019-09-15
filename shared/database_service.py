import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebase_admin.initialize_app(credentials.ApplicationDefault(), {'projectId': 'image-post',})
db = firestore.client()


def get_data(collection_name):
    collection = db.collection(collection_name).stream()
    result = []

    for doc in collection:
        result.append(doc.to_dict())

    return result


def create_data(collection, data):
    ref = db.collection(collection).document()
    ref.set(data)


def get_all_used_quotes():
    data_list = get_data('usedQuotes')

    result = []
    for data in data_list:
        result.append(data['quote'])

    return result


def set_new_quote(quote):
    create_data('usedQuotes', {'quote': quote})


def get_font_configurations():
    return get_data('fontConfiguration')


def get_font_configuration_by_name(font_name):
    with open('db.json', "r") as used_quotes:
        data = json.load(used_quotes)

    return [config for config in data['font_configuration'] if config['fontName'] == font_name][0]


def set_used_image(url):
    create_data('usedImages', {'imageURL': url})


def get_all_used_images():
    data_list = get_data('usedImages')

    result = []
    for data in data_list:
        result.append(data['imageURL'])

    return result


def get_quotes_routes():
    data_list = get_data('quotesSource')

    result = []
    for data in data_list:
        result.append(data['route'])

    return result


def set_json(quote):
    with open('db.json', "r+") as used_quotes:
        data = json.load(used_quotes)
        data['used_quotes'].append(quote)
        used_quotes.seek(0)  # rewind
        json.dump(data, used_quotes, indent=2)
        used_quotes.truncate()
