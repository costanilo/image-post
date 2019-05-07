from googleapiclient.discovery import build

import json
import pprint
import urllib.request

def dowload_image_by_text(text):
    with open('config.json') as config_file:
        data = json.load(config_file)

    service = build("customsearch", "v1", developerKey=data['apiKey'])

    res = service.cse().list(
        cx=data['searchEngineId'],
        q=text,
        searchType='image',
        imgSize='large',
        num=1,
        imgType='photo',
        imgDominantColor='black'
    ).execute()

    image_link = res['items'][0]['link']
    file_name = 'base-picture.jpeg'

    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(image_link, file_name)
