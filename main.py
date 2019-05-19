from services.quotes_service import get_some_quote
from services.google_service import dowload_image_by_text
from services.image_service import create_image_quote
from services.facebook_service import post_image_on_facebook

import os
import json
import time

for x in range(20):
    print(x)
    quote = get_some_quote(False)

    dowload_image_by_text(quote.author)

    create_image_quote(quote)

    post_image_on_facebook('Siga: @nessasfrasesdavida')

    time.sleep(5)

    # os.system("start new-picture-" + str(1) + ".png")
