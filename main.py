from services.quotes_service import get_some_quote
from services.google_service import dowload_image_by_text
from services.image_service import print_text_on_image_and_save
from services.facebook_service import post_image_on_facebook

import os
import json

# for x in range(19):
#     print(x)
quote = get_some_quote(False)

#dowload_image_by_text(quote.author)

print_text_on_image_and_save(quote, x=1)

post_image_on_facebook('Para refletir...')

#os.system("start new-picture-" + str(x) + ".png")
