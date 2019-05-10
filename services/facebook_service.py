from shared.configuration_service import get_config_by_key

import facebook
import json

def post_image_on_facebook(subtitle):
    app_token = get_config_by_key('facebookUserToken')
    graph = facebook.GraphAPI(app_token)
    graph.put_photo(image=open('new-picture.png', 'rb'), message=subtitle)
