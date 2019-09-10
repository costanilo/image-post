from googleapiclient.discovery import build
from shared.configuration_service import get_config_by_key
from shared.proxy_service import download_link
from shared.database_service import get_all_used_images, set_used_image

import pprint

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def analyze_text():
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    text = u'Everyone is capable of mastering a pain except who feels it.'
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT,
        )

    # Detects the sentiment of the text
    sentiment = client.analyze_entities(document=document)

    pprint.pprint(sentiment)
    # print('Text: {}'.format(text))
    # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


def download_image_by_text(text):
    print("Searching for images...")
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

    image_links = res['items']
    used_links = get_all_used_images()

    print("Choosing Image...")
    for image in image_links:
        if image['link'] not in used_links:
            download_link(image['link'], 'base-picture.png')
            set_used_image(image['link'])
            print("Image Saved!...")
            break
