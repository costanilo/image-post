import json


def get_config_by_key(key):
    with open('config.json') as config_file:
        data = json.load(config_file)

    return '' if data[key] is None else data[key]
