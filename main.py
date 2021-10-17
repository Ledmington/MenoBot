from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

import logging
import os

import help # Command
import cards_list # Command
import search # Command
from bot_states import States

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
			CommandHandler('help', help.help_command),
			CommandHandler('list_most_wanted_cards', cards_list.get_most_wanted_cards),
			CommandHandler('list_my_cards', cards_list.get_my_cards),
			CommandHandler('add_card', cards_list.add_card),
			CommandHandler('remove_card', cards_list.remove_card),
			CommandHandler('search', search.search_card),
			CommandHandler('update_all_prices', cards_list.update_all_prices),
			CommandHandler('update_price', cards_list.update_price_command)
		],
		states = {
			States.WAITING_TO_ADD_CARD: [MessageHandler(Filters.regex(r"\d+"), cards_list.save_new_card)]
		},
		fallbacks = []
	)

	dispatcher.add_handler(conv_handler)

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		print("Waiting for price-updater thread to die...")
		global need_to_be_alive
		cards_list.need_to_be_alive = False
		global price_updater_thread
		cards_list.price_updater_thread.join()