from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters,
)

import logging
import os
import sys
import time
from datetime import datetime

import help  # Command
import cards_list  # Command
import search  # Command
from bot_states import States

import user
from menobot.utils.formatter import CustomFormatter
from menobot.utils.worker import Worker

price_updater_thread = None


def setup_logger():
    # create logs directory
    if not os.path.exists("logs"):
        os.mkdir("logs")

    logger = logging.getLogger("menobot")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s]: %(message)s", "%m-%d-%Y %H:%M:%S"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter())

    file_handler = logging.FileHandler("logs/menobot.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def main() -> None:
    token_filename = "telegram_token"
    if not os.path.exists(token_filename):
        print(f'File "{token_filename}" not found.\nQuitting...')
        quit()

    # Reading token
    with open(token_filename, "r") as token_file:
        mytoken = token_file.read()

    setup_logger()
    logger = logging.getLogger("menobot")
    logger.info("Started new session")

    updater = Updater(token=mytoken, use_context=True)
    dispatcher = updater.dispatcher

    logger.info("Initialized scheduler")

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            CommandHandler("help", help.help_command),
            CommandHandler("list_most_wanted_cards", cards_list.get_most_wanted_cards),
            CommandHandler("list_my_cards", cards_list.get_my_cards),
            CommandHandler("add", cards_list.add_command),
            CommandHandler("remove", cards_list.remove_command),
            CommandHandler("search", search.search_command),
            CommandHandler("update_all_prices", cards_list.update_all_prices_command),
            CommandHandler("update_price", cards_list.update_price_command),
            CommandHandler("set_timeout", cards_list.set_timeout),
        ],
        states={
            States.WAITING_TO_SEARCH_CARD: [
                MessageHandler(
                    Filters.regex(r"[\w\s\d\-\.\,\?\!\:\@\'\&\/\(\)]+"),
                    cards_list.add_card,
                )
            ],
            States.WAITING_TO_ADD_CARD: [
                MessageHandler(Filters.regex(r"\d+"), cards_list.save_new_card)
            ],
            States.WAITING_TO_REMOVE_CARD: [
                MessageHandler(Filters.regex(r"\d+"), cards_list.remove_card)
            ],
            States.WAITING_CARD_TO_SEARCH: [
                MessageHandler(
                    Filters.regex(r"[\w\s\d\-\.\,\?\!\:\@\'\&\/\(\)]+"),
                    search.search_card,
                )
            ],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    logger.info("Creating price updater thread")
    price_updater_thread = Worker(price_update_loop)
    price_updater_thread.start()
    logger.info("Price updater thread created")

    logger.info("MenoBot ready")

    updater.start_polling()
    updater.idle()


def price_update_loop():
    logger = logging.getLogger("menobot")
    for uid, u in user.users.items():
        if (datetime.now() - u.last_update).seconds >= u.timeout_seconds:
            logger.info(f"Updating prices for user {uid}")
            u.update_all_prices()  # absolutely change this
    time.sleep(10)


def start_command(update, context):
    logger = logging.getLogger("menobot")
    user_id = update.effective_chat.id
    logger.info(f"Received /start from {user_id}")
    if user_id not in user.users.keys():
        user.users[user_id] = user.User(user_id)
        logger.info(f"New User created with id {user_id}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Welcome to MenoBot, a Telegram bot designed to monitor price fluctuations of YuGiOh cards on cardmarket.\nYour ID is "
            + str(user_id),
        )
    else:
        logger.info(f"User with id {user_id} was already present")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are already registered.\nYour ID is " + str(user_id),
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        logger = logging.getLogger("menobot")
        logger.info("Waiting for price updater thread to die")
        price_updater_thread.join()
        logger.info("price updater thread is dead")

        logger.info("End session\n")
