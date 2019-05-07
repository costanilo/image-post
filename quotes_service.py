import pprint
import urllib.request
import ftfy.bad_codecs
import re
import os

from bs4 import BeautifulSoup
from ftfy import fix_text, fix_encoding
from ftfy.fixes import restore_byte_a0


def get_some_quote():
    # opener=urllib.request.build_opener()
    # opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    # urllib.request.install_opener(opener)

    fp = urllib.request.urlopen("https://www.pensador.com/populares/1/")
    mybytes = fp.read()
    mybytes = restore_byte_a0(mybytes)
    mystr = mybytes.decode('utf-8')

    fp.close()
    soup = BeautifulSoup(mystr, "lxml")

    quotes = soup.findAll("p", {"class": "frase"})
    authors = soup.findAll("span", {"class": "autor"})

    selected_quote = ''
    selected_author = ''


    for quote in quotes:
        if len(quote.get_text()) <= 300:
            selected_quote = quote.get_text(strip=True)
            selected_author = authors[quotes.index(quote)].get_text(strip=True)

    return [selected_quote, selected_author]
