from quotes_service import get_some_quote
from google_service import dowload_image_by_text
from image_service import print_text_on_image_and_save
from facebook_service import post_image_on_facebook

quote_and_author = get_some_quote()

dowload_image_by_text(quote_and_author[1])

print_text_on_image_and_save(quote_and_author[0] + '\n\n' + quote_and_author[1])

post_image_on_facebook('works baby!')

