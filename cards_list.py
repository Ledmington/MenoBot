from telegram.ext import ConversationHandler
import utils
import re
from bot_states import States

interesting_cards = []
retrieved_cards = []

def get_most_wanted_cards(update, context):
	page_content = utils.download_html(utils.CardMarketURLs["cards_list"])
	cards = utils.parse_cards(page_content)

	message = utils.compose_list(cards)
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML", disable_web_page_preview=True)

def get_my_cards(update, context):
	global interesting_cards
	if len(interesting_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You are following 0 cards.")
		return

	message = "You are following " + str(len(interesting_cards)) + " cards.\n" + utils.compose_list(retrieved_cards, with_index=True)

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML", disable_web_page_preview=True)

def add_card(update, context) -> int:
	if len(context.args) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No card name given.")
		return

	query_string = "+".join(context.args)
	page_content = utils.download_html(utils.CardMarketURLs["search_query"] + query_string)

	global retrieved_cards
	retrieved_cards = utils.parse_cards(page_content)

	if len(retrieved_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No cards found.")
		return

	# We keep only the first 5 results (the number should be global and changeable)
	retrieved_cards = retrieved_cards[:5]
	
	message = utils.compose_list(retrieved_cards, with_index=True) + "\nPlease type a number from 1 to " + str(len(retrieved_cards)) + " to choose that card."

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML", disable_web_page_preview=True)

	return States.WAITING_TO_ADD_CARD

def save_new_card(update, context) -> int:
	selected_card = int(update.message.text)-1

	if selected_card >= len(retrieved_cards):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid card number.\nTry another one.")
		return States.WAITING_TO_ADD_CARD

	global interesting_cards
	interesting_cards.append(retrieved_cards[selected_card])
	interesting_cards = list(set(interesting_cards))

	message = "<b>" + retrieved_cards[selected_card][0] + "</b> added to list."

	message += "\nCurrent price: " + str(utils.get_price(utils.CardMarketURLs["base"]+retrieved_cards[selected_card][1])) + " €"

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

	return ConversationHandler.END

def remove_card(update, context):
	input_string = " ".join(context.args)

	if not re.match(r"\d+", input_string):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid number.")
		return

	selected_card = int(input_string)-1

	global interesting_cards
	if len(interesting_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You have no cards to remove.")
		return

	if selected_card >= len(interesting_cards):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid card number.\nTry another one.")
		return

	removed_card = interesting_cards.pop(selected_card)

	message = "<b>" + removed_card[0] + "</b> removed from list."

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")