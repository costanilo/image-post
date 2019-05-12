from googleapiclient.discovery import build
from shared.configuration_service import get_config_by_key
from shared.proxy_service import download_link
from shared.database_service import get_all_used_images, set_used_image

import pprint
import json

def dowload_image_by_text(text):
    api_key = get_config_by_key('apiKey')
    engine_id = get_config_by_key('searchEngineId')
    service = build("customsearch", "v1", developerKey=api_key)

    text = text if text.upper() != 'DESCONHECIDO' else 'Paisagem'

    res = service.cse().list(
        cx=engine_id,
        q=text,
        searchType='image',
        imgSize='large',
        num=10,
        imgType='photo'
    ).execute()
    # pprint.pprint(res)

    # with open('images.json', 'w') as outfile:  
    #     json.dump(res, outfile)

    image_links = res['items'] #[0]['link']
    used_links = get_all_used_images()

    for image in image_links:
        if image['link'] not in used_links:
            download_link(image['link'], 'base-picture.png')
            set_used_image(image['link'])
            break
