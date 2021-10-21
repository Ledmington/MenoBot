from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

import logging
import os

import help # Command
import cards_list # Command
import search # Command
from bot_states import States

import user

def main() -> None:
	if not os.path.exists("token"):
		print("File \"token\" not found.\nQuitting...")
		quit()

	# Reading token
	with open("token", "r") as token_file:
		mytoken = token_file.read()

	updater = Updater(token=mytoken, use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	conv_handler = ConversationHandler(
		entry_points = [
			CommandHandler('start', start_command),
			CommandHandler('help', help.help_command),
			CommandHandler('list_most_wanted_cards', cards_list.get_most_wanted_cards),
			CommandHandler('list_my_cards', cards_list.get_my_cards),
			CommandHandler('add', cards_list.add_command),
			CommandHandler('remove', cards_list.remove_command),
			CommandHandler('search', search.search_card),
			CommandHandler('update_all_prices', cards_list.update_all_prices_command),
			CommandHandler('update_price', cards_list.update_price_command),
			CommandHandler('set_timeout', cards_list.set_timeout)
		],
		states = {
			States.WAITING_TO_SEARCH_CARD: [MessageHandler(Filters.regex(r"[\w\s\d\-\.\,\?\!\:\@\'\&\/\(\)]+"), cards_list.add_card)],
			States.WAITING_TO_ADD_CARD: [MessageHandler(Filters.regex(r"\d+"), cards_list.save_new_card)],
			States.WAITING_TO_REMOVE_CARD: [MessageHandler(Filters.regex(r"\d+"), cards_list.remove_card)]
		},
		fallbacks = []
	)

	dispatcher.add_handler(conv_handler)

	updater.start_polling()
	updater.idle()

def start_command(update, context):
	user_id = update.effective_chat.id
	if user_id not in user.users.keys():
		user.users[user_id] = user.User(user_id)
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You are already registered.\nYour ID is " + str(user_id))

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		users_to_kill = list(user.users.values())
		print(str(len(users_to_kill)) + " price-updater threads to kill\n")
		for u in users_to_kill:
			u.thread_needs_to_be_alive = False

		for u in users_to_kill:
			if u.price_updater_thread is not None:
				print("[" + str(users_to_kill.index(u)+1) + "/" + str(len(users_to_kill)) + "] Waiting for price-updater thread to die...")
				u.price_updater_thread.join()