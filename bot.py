from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am MenoBot.")

updater = Updater(token='1917043976:AAFylwCoNSLUp230XHM_o_hUovpKJFnU164', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()