from services.quotes_service import get_some_quote
from services.google_service import dowload_image_by_text
from services.image_service import print_text_on_image_and_save
from services.facebook_service import post_image_on_facebook

import os
import json

quote_and_author = get_some_quote()

dowload_image_by_text(quote_and_author[1])

print_text_on_image_and_save(quote_and_author[0] + '\n\n' + quote_and_author[1])

post_image_on_facebook('Para refletir...')

