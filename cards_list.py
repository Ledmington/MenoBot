from telegram.ext import ConversationHandler
import utils
import re
from bot_states import States
from card import Card
import threading
import datetime
import time

interesting_cards = []
retrieved_cards = []

need_to_be_alive = True
price_updater_thread = None

# minimum timeout: 10 minutes
def update_all_prices(timeout=600):
	time_passed = 0
	while need_to_be_alive == True:
		time.sleep(10)
		time_passed += 10
		if(time_passed >= timeout):
			time_passed = 0
			print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Started update")
			for c in interesting_cards:
				new_price = utils.download_price(c.get_url())
				c.update_price(new_price)
				print("New price for \"" + c.get_name() + "\": " + str(new_price) + " €")
			print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Finished update\n")

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

	message = "You are following " + str(len(interesting_cards)) + " cards.\n" + utils.compose_list(interesting_cards, with_index=True)
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
	new_card = Card(retrieved_cards[selected_card][0], utils.CardMarketURLs["base"]+retrieved_cards[selected_card][1])
	interesting_cards.append(new_card)
	interesting_cards = list(set(interesting_cards))

	message = "<b>" + retrieved_cards[selected_card][0] + "</b> added to list."
	current_price = utils.download_price(new_card.get_url())
	new_card.update_price(current_price)
	message += "\nCurrent price: " + str(current_price) + " €"

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

	global price_updater_thread
	if price_updater_thread == None:
		price_updater_thread = threading.Thread(target=update_all_prices, args=(10,))
		price_updater_thread.start()

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