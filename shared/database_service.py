import json

def get_all_used_quotes():
    with open('used_quotes.json', "r") as used_quotes:
        data = json.load(used_quotes)

    return data['used']

def set_new_quote(quote):
    with open('used_quotes.json', "r+") as used_quotes:
        data = json.load(used_quotes)
        data['used'].append(quote)
        used_quotes.seek(0)  # rewind
        json.dump(data, used_quotes, indent=2)
        used_quotes.truncate()