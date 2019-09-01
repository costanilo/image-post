from bs4 import BeautifulSoup
from ftfy import fix_text, fix_encoding
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


def get_some_quote(is_mock):
    if is_mock:
        mock_quote = Quote()
        mock_quote.author = "Augusto Branco"
        mock_quote.text = "A maior covardia de um homem é despertar o amor de uma mulher sem ter a intenção de amá-la."
        return mock_quote

    url = get_config_by_key('quotesSource')

    selected_quote = Quote()

    not_used_routes = get_config_by_key('quotesRoutes')

    while selected_quote.text == '' and len(not_used_routes) > 0:
        index = 0
        current_route = not_used_routes.pop(index)

        html_page = get_html_page(url + current_route)
        soup = BeautifulSoup(html_page, "html.parser")

        quotes = soup.findAll("p", {"class": "frase"})
        authors = soup.findAll("span", {"class": "autor"})

        used_quotes = get_all_used_quotes()

        for quote in quotes:
            if quote.get_text() not in used_quotes and len(quote.get_text(strip=True)) <= 240:
                selected_quote.text = quote.get_text()
                selected_quote.author = authors[quotes.index(
                    quote)].get_text(strip=True)
                break

        index += 1

    if selected_quote.text == '':
        raise Exception('Não foi possível encontrar nenhuma frase nas rotas configuradas')

    set_new_quote(selected_quote.text)

    return selected_quote
