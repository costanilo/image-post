from shared.configuration_service import get_config_by_key

import facebook
import json
import requests

def post_image_on_facebook():
    graph = facebook.GraphAPI(get_config_by_key('facebookUserToken'))
    graph.put_photo(image=open('new-picture.png', 'rb'), message="")

def log_in():
    app_id = get_config_by_key('facebookId')
    app_secret = get_config_by_key('facebookSecret')
    user_short_token = get_config_by_key('facebookUserToken')
    access_token_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(app_id, app_secret, user_short_token)
    r = requests.get(access_token_url)
    access_token_info = r.json()
    user_long_token = access_token_info['access_token']
    graph = facebook.GraphAPI(user_long_token)
    pages_data = graph.get_object("/me/accounts")
    print(pages_data)