from services.quotes_service import get_some_quote
from services.google_service import download_image_by_text, analyze_text
from services.image_service import create_image_quote
from services.facebook_service import post_image_on_facebook, log_in

import os
import json
import time


def publish_process():
    # quote = get_some_quote(False)
    # download_image_by_text(quote.author)
    # create_image_quote(quote)
    post_image_on_facebook()
    # time.sleep(5)
    #
    # os.system("start new-picture-" + str(1) + ".png")
