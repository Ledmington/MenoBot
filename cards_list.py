from telegram.ext import ConversationHandler
import utils

WAITING_TO_ADD_CARD = 1

interesting_cards = set()
retrieved_cards = []
base_url = "https://www.cardmarket.com"

def get_most_wanted_cards(update, context):
	cards_list_url = "https://www.cardmarket.com/en/YuGiOh/Products/Singles"

	page_content = utils.download_html(cards_list_url)
	cards = utils.parse_cards(page_content)

	message = ""
	for c in cards:
		message += "<a href=\"" + base_url + c[1] + "\">" + c[0] + "</a>\n"
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

def get_my_cards(update, context):
	global interesting_cards
	if len(interesting_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You are following 0 cards.")
		return

	message = "You are following " + str(len(interesting_cards)) + " cards.\n"
	for c in interesting_cards:
		message += "<a href=\"" + base_url + c[1] + "\">" + c[0] + "</a>\n"
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

def add_card(update, context) -> int:
	search_query = "https://www.cardmarket.com/en/YuGiOh/Products/Singles?idCategory=5&idExpansion=0&idRarity=0&searchString="

	if len(context.args) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No card name given.")
		return

	query_string = "+".join(context.args)
	page_content = utils.download_html(search_query + query_string)

	global retrieved_cards
	retrieved_cards = utils.parse_cards(page_content)

	if len(retrieved_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No cards found.")
		return

	# We keep only the first 5 results (the number should be global and changeable)
	retrieved_cards = retrieved_cards[:5]
	
	message = ""
	for c in retrieved_cards:
		message += "<b>" + str(retrieved_cards.index(c)+1) + "</b> <a href=\"" + base_url + c[1] + "\">" + c[0] + "</a>\n"

	message += "\nPlease type a number from 1 to " + str(len(retrieved_cards)) + " to choose that card."

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

	return WAITING_TO_ADD_CARD

def save_new_card(update, context) -> int:
	selected_card = int(update.message.text)-1

	if selected_card >= len(retrieved_cards):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid card number.\nTry another one.")
		return WAITING_TO_ADD_CARD

	global interesting_cards
	interesting_cards.add(retrieved_cards[selected_card])

	message = "<b>" + retrieved_cards[selected_card][0] + "</b> added to list."

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

	return ConversationHandler.END