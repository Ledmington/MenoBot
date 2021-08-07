from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, benvenuto su MenoBot 0.1")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I comandi disponibili sono:\n/start\n/help")

def main() -> None:
	updater = Updater(token='1917043976:AAFylwCoNSLUp230XHM_o_hUovpKJFnU164', use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)

	help_handler = MessageHandler(Filters.text & (~Filters.command), help)
	dispatcher.add_handler(help_handler)
	help_handler2 = CommandHandler('help', help)
	dispatcher.add_handler(help_handler2)

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()