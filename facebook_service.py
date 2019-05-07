import facebook
import json

def post_image_on_facebook(subtitle):
    with open('config.json') as config_file:
        data = json.load(config_file)

    app_token = data['facebookUserToken']

    graph = facebook.GraphAPI(app_token)

    graph.put_photo(image=open('new-picture.jpg', 'rb'), message=subtitle)
