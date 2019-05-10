from googleapiclient.discovery import build
from shared.configuration_service import get_config_by_key
from shared.proxy_service import download_link

import pprint

def dowload_image_by_text(text):
    api_key = get_config_by_key('apiKey')
    engine_id = get_config_by_key('searchEngineId')
    service = build("customsearch", "v1", developerKey=api_key)

    res = service.cse().list(
        cx=engine_id,
        q=text,
        searchType='image',
        imgSize='large',
        num=10,
        imgType='photo'
    ).execute()

    image_link = res['items'][0]['link']
    file_name = 'base-picture.png'
    download_link(image_link, file_name)


