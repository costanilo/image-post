from bs4 import BeautifulSoup
from shared.proxy_service import get_html_page
from shared.database_service import get_all_used_quotes, set_new_quote, get_quotes_routes
from models.quote_model import Quote

QUOTE_SOURCE = "https://www.pensador.com/"


def get_some_quote():
    print("Searching quote...")
    url = QUOTE_SOURCE
    selected_quote = Quote()
    not_used_routes = get_quotes_routes()

    while selected_quote.text == '' and len(not_used_routes) > 0:
        index = 0
        current_route = not_used_routes.pop(index)

        print("Getting page in route '{0}'...".format(current_route))

        html_page = get_html_page(url + current_route)
        soup = BeautifulSoup(html_page, "html.parser")

        quotes = soup.findAll("p", {"class": "frase"})
        authors = soup.findAll("span", {"class": "autor"})

        used_quotes = get_all_used_quotes()

        print("Searching for new quote...")
        for quote in quotes:
            if quote.get_text() not in used_quotes and len(quote.get_text(strip=True)) <= 240:
                print("Quote found!")
                selected_quote.text = quote.get_text()
                selected_quote.author = authors[quotes.index(quote)].get_text(strip=True)
                break
        if selected_quote.text == '':
            print("No new quotes found in route...")
        index += 1

    if selected_quote.text == '':
        raise Exception('ERROR: No quotes not used before found in configured routes')

    set_new_quote(selected_quote.text)

    return selected_quote
