import urllib.request
from urllib.error import HTTPError,URLError
import re

import cards_list

def search_card(update, context):
	base_url = "https://www.cardmarket.com"
	search_query = "https://www.cardmarket.com/en/YuGiOh/Products/Singles?idCategory=5&idExpansion=0&idRarity=0&searchString="

	if len(context.args) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No query given.")
		return

	query_string = "+".join(context.args)

	try:
		response = urllib.request.urlopen(search_query + query_string)
	except (HTTPError, URLError) as error:
		logging.error(" Data of \"%s\" not retrieved because %s\n", search_query + query_string, error)
	except ValueError:
		logging.error(" Unknown url type\n")

	page_content = response.read().decode("utf-8")

	cards = cards_list.parse_cards(page_content)

	if len(cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No cards found.")
		return

	# We keep only the first 5 results (the number should be global and changeable)
	cards = cards[:5]
	message = ""
	for c in cards:
		message = message + "<a href=\"" + base_url + c[1] + "\">" + c[0] + "</a>\n"
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")