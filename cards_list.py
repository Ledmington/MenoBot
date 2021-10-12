import urllib.request
from urllib.error import HTTPError,URLError
import re

cards_regex = re.compile("(<a href=\"\S*\">[\w\s\d\-\.\,\?\!\:\@\'\&\/]+<\/a>)")

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

def get_cards_list(update, context):
	main_page_url = "https://www.cardmarket.com/en/YuGiOh"
	cards_list_url = "https://www.cardmarket.com/en/YuGiOh/Products/Singles"
	base_url = "https://www.cardmarket.com"

	try:
		response = urllib.request.urlopen(cards_list_url)
	except (HTTPError, URLError) as error:
		logging.error(" Data of \"%s\" not retrieved because %s\n", cards_list_url, error)
	except ValueError:
		logging.error(" Unknown url type\n")

	page_content = response.read().decode("utf-8")

	cards = parse_cards(page_content)
	message = ""
	for c in cards:
		message = message + c[0] + " (" + base_url + c[1] + ")\n"
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)