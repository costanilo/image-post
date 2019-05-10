from bs4 import BeautifulSoup
from ftfy import fix_text, fix_encoding
from ftfy.fixes import restore_byte_a0
from shared.configuration_service import get_config_by_key
from shared.proxy_service import get_html_page
from shared.database_service import get_all_used_quotes, set_new_quote
from models.quote_model import Quote

import pprint
import urllib.request
import ftfy.bad_codecs
import re
import os
import json


def get_some_quote():
    url = get_config_by_key('quotesSource')

    html_page = get_html_page(url)

    soup = BeautifulSoup(html_page, "lxml")

    quotes = soup.findAll("p", {"class": "frase"})
    authors = soup.findAll("span", {"class": "autor"})

    selected_quote = Quote()

    used_quotes = get_all_used_quotes()

    for quote in quotes:
        if quote.get_text() not in used_quotes and len(quote.get_text()) <= 300:
            selected_quote.text = '"' + quote.get_text() + '"'
            selected_quote.author = authors[quotes.index(quote)].get_text(strip=True)
            break

    #set_new_quote(selected_quote)


    return selected_quote
