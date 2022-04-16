from telegram.ext import ConversationHandler

import utils
from bot_states import States


def search_command(update, context) -> int:
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Type the name of a card to search."
    )
    return States.WAITING_CARD_TO_SEARCH


def search_card(update, context) -> int:

    query_string = "+".join(update.message.text)
    page_content = utils.download_html(
        utils.CardMarketURLs["search_query"] + query_string
    )

    cards = utils.parse_cards(page_content)

    if len(cards) == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="No cards found."
        )
        return

    # We keep only the first 5 results (the number should be global and changeable)
    cards = cards[:5]

    message = utils.compose_list(cards)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    return ConversationHandler.END
