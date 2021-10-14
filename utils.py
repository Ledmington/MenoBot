import urllib.request
from urllib.error import HTTPError,URLError
import re

cards_regex = re.compile(r"(<a href=\"\S*\">[\w\s\d\-\.\,\?\!\:\@\'\&\/\(\)]+<\/a>)")

CardMarketURLs = {
	"base": "https://www.cardmarket.com",
	"cards_list": "https://www.cardmarket.com/en/YuGiOh/Products/Singles",
	"search_query": "https://www.cardmarket.com/en/YuGiOh/Products/Singles?idCategory=5&idExpansion=0&idRarity=0&searchString="
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

def download_html(page_url):
	try:
		response = urllib.request.urlopen(page_url)
	except (HTTPError, URLError) as error:
		logging.error(" Data of \"%s\" not retrieved because %s\n", page_url, error)
	except ValueError:
		logging.error(" Unknown url type\n")

	page_content = response.read().decode("utf-8")
	return page_content

def compose_list(cards, with_index=False):
	message = ""
	for c in cards:
		if with_index:
			message += "<b>" + str(cards.index(c)+1) + "</b> "
		message += "<a href=\"" + CardMarketURLs["base"] + c[1] + "\">" + c[0] + "</a>\n"

	return message