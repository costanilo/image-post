import os


def get_config_by_key(key):
    data = os.environ.get(key)
    print("Getting environment: {0}".format(key))
    return '' if data is None else data
