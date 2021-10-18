from telegram.ext import ConversationHandler
import utils
import re
from bot_states import States
from card import Card
import threading
import datetime
import time

import user

need_to_be_alive = True
price_updater_thread = None

min_timeout = 600   # 10 minutes
max_timeout = 86400 # 24 hours

# minimum timeout: 10 minutes
def updater_thread_function(update, context):
	time_passed = 0
	while need_to_be_alive == True:
		if(time_passed >= timeout_seconds):
			time_passed = 0
			update_all_prices(update, context)
		time.sleep(10)
		time_passed += 10

def set_timeout(update, context):
	input_string = " ".join(context.args)
	timeout_regex = r"(\d\d?)(m|h)"

	if not re.match(timeout_regex, input_string):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid format.\nType a number and then \"m\" for minutes or \"h\" for hours.")
		return

	results = re.match(timeout_regex, input_string).groups()
	new_timeout = int(results[0])
	if results[1] == "m":
		new_timeout *= 60
	elif results[1] == "h":
		new_timeout *= 60*60

	if new_timeout<min_timeout or new_timeout>max_timeout:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid value.\nTimeout must be between 10 minutes and 24 hours.")
		return

	timeout_seconds = new_timeout

def update_all_prices(update, context):
	for c in interesting_cards:
		force_update_price(c)

def force_update_price(card):
	new_price = utils.download_price(card.get_url())
	card.update_price(new_price)

def update_price_command(update, context):
	input_string = " ".join(context.args)

	if not re.match(r"\d+", input_string):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid number.")
		return

	selected_card = int(input_string)-1

	global interesting_cards
	if len(interesting_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You have no cards.")
		return

	if selected_card >= len(interesting_cards):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid card number.\nTry another one.")
		return

	force_update_price(interesting_cards[selected_card])

def get_most_wanted_cards(update, context):
	page_content = utils.download_html(utils.CardMarketURLs["cards_list"])
	cards = utils.parse_cards(page_content)

	message = utils.compose_list(cards)
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML", disable_web_page_preview=True)

def get_my_cards(update, context):
	my_cards = user.users[update.effective_chat.id].get_interesting_cards()
	if len(my_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You are following 0 cards.")
		return

	message = "You are following " + str(len(my_cards)) + " cards.\n" + utils.compose_list(my_cards, with_index=True)
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML", disable_web_page_preview=True)

def add_card(update, context) -> int:
	if len(context.args) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No card name given.")
		return

	query_string = "+".join(context.args)
	page_content = utils.download_html(utils.CardMarketURLs["search_query"] + query_string)

	current_user = user.users[update.effective_chat.id]
	current_user.retrieved_cards = utils.parse_cards(page_content)

	if len(current_user.retrieved_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No cards found.")
		return

	# We keep only the first 5 results (the number should be global and changeable)
	current_user.retrieved_cards = current_user.retrieved_cards[:5]
	
	message = utils.compose_list(current_user.retrieved_cards, with_index=True) + "\nPlease type a number from 1 to " + str(len(current_user.retrieved_cards)) + " to choose that card."

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML", disable_web_page_preview=True)

	return States.WAITING_TO_ADD_CARD

def save_new_card(update, context) -> int:
	selected_card = int(update.message.text)-1
	current_user = user.users[update.effective_chat.id]

	if selected_card >= len(current_user.retrieved_cards):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid card number.\nTry another one.")
		return States.WAITING_TO_ADD_CARD

	new_card = Card(current_user.retrieved_cards[selected_card][0], utils.CardMarketURLs["base"]+current_user.retrieved_cards[selected_card][1])
	current_user.add_card(new_card)

	message = "<b>" + current_user.retrieved_cards[selected_card][0] + "</b> added to list."
	current_price = utils.download_price(new_card.get_url())
	new_card.update_price(current_price)
	message += "\nCurrent price: " + str(current_price) + " €"

	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

	global price_updater_thread
	if price_updater_thread == None:
		price_updater_thread = threading.Thread(target=updater_thread_function, args=(update, context,))
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