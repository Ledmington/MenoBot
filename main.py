from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import logging

import help # Command
import start # Command
import cards_list # Command

def main() -> None:
	# Reading token
	with open("token", "r") as token_file:
		mytoken = token_file.read()

	updater = Updater(token=mytoken, use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	start_handler = CommandHandler('start', start.start_command)
	dispatcher.add_handler(start_handler)

	help_handler = CommandHandler('help', help.help_command)
	dispatcher.add_handler(help_handler)

	html_handler = CommandHandler('list_most_wanted_cards', cards_list.get_cards_list)
	dispatcher.add_handler(html_handler)

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()