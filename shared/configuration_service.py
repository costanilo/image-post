import json
import os


def get_config_by_key(key):
    # with open('config.json') as config_file:
    #     data = json.load(config_file)
    # return '' if data[key] is None else data[key]
    data = os.environ.get(key)
    print("Getting environment: {0}".format(key))
    return '' if data is None else data
