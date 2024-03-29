import urllib.request
from urllib.error import HTTPError, URLError
import re
import logging

from menobot.menobot.card import Card

cards_regex = re.compile(r"(<a href=\"\S*\">[\w\s\d\-\.\,\?\!\:\@\'\&\/\(\)]+<\/a>)")

CardMarketURLs = {
    "base": "https://www.cardmarket.com",
    "cards_list": "https://www.cardmarket.com/en/YuGiOh/Products/Singles",
    "search_query": "https://www.cardmarket.com/en/YuGiOh/Products/Singles?idCategory=5&idExpansion=0&idRarity=0&searchString=",
}


def parse_cards(html_code):
    cards = cards_regex.findall(html_code)
    card_names = []
    for c in cards:
        str_split = re.split(r"[<>]", c)
        card_link = re.split(r"\"", str_split[1])[1]
        card_name = str_split[2]
        if card_name == "Mystic Mine":
            print("Fuck You Mystic Mine")
        else:
            card_names.append((card_name, card_link))

    # The first two are always "Privacy Policy" and "About Us"
    card_names = card_names[2:]
    return card_names


def download_price(card_page_url):
    page_html = download_html(card_page_url)

    # The "price trend" price is the second shown on page
    price_match = re.findall(r"(\d+,\d\d) €", page_html)[1]

    if price_match is None:
        logging.error(' Price not found in "' + card_page_url + '"\n')
        return

    # Converting "x,yz €" to "x.yz"
    price = float(price_match.replace(",", "."))

    return price


def download_html(page_url):
    page_content = ""

    try:
        response = urllib.request.urlopen(page_url)
        page_content = response.read().decode("utf-8")
    except (HTTPError, URLError) as error:
        logging.error(' Data of "%s" not retrieved because %s\n', page_url, error)
    except ValueError:
        logging.error(" Unknown url type\n")

    return page_content


def compose_list(cards, with_index=False):
    message = ""
    for c in cards:
        if with_index:
            message += "<b>" + str(cards.index(c) + 1) + "</b> "
        if type(c) == type(Card("", "")):
            message += '<a href="' + c.get_url() + '">' + c.get_name() + "</a>\n"
        else:
            message += (
                '<a href="' + CardMarketURLs["base"] + c[1] + '">' + c[0] + "</a>\n"
            )

    return message
