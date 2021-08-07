from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, benvenuto su MenoBot 0.1")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main() -> None:
	updater = Updater(token='1917043976:AAFylwCoNSLUp230XHM_o_hUovpKJFnU164', use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)

	echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
	dispatcher.add_handler(echo_handler)

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()