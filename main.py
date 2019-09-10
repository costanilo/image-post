from services.quotes_service import get_some_quote
from services.google_service import download_image_by_text, analyze_text
from services.image_service import create_image_quote
from services.facebook_service import post_image_on_facebook

print("Starting process!")
quote = get_some_quote()
download_image_by_text(quote.author)
create_image_quote(quote)
post_image_on_facebook()
print("Process finished!")
