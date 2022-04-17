from datetime import datetime
import logging

from menobot.utils import utils

users = {}
logger = logging.getLogger("menobot")


class User:
    price_difference = 0.01  # 1%
    timeout_seconds = 600  # 10 minutes

    def __init__(self, new_id):
        if new_id <= 0:
            logger.exception(f"Attempting to create a User with id {new_id}")
            raise ValueError("User Id cannot be zero or negative")
        self.user_id = new_id
        self.retrieved_cards = []
        self.interesting_cards = []
        last_update = datetime.now()

    def get_interesting_cards(self):
        return self.interesting_cards

    def add_card(self, new_card, update, context):
        self.interesting_cards.append(new_card)
        self.interesting_cards = list(set(self.interesting_cards))

    def update_all_prices(self, update, context):
        print(
            "["
            + str(datetime.datetime.now())
            + "] Called update_all_prices from "
            + str(self.user_id)
        )
        message = ""
        for c in self.interesting_cards:
            price_changed = self.force_update_price(c)
            if price_changed != 0:
                message += (
                    '<a href="' + c.get_url() + '"><b>' + c.get_name() + "</b></a> has "
                )
                if price_changed > 0:
                    message += "increased"
                else:
                    message += "decreased"
                message += (
                    " price to " + str(c.get_last_update()).replace(".", ",") + " €\n"
                )

        if len(message) > 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )

    def force_update_price(self, card):
        new_price = utils.download_price(card.get_url())
        last_price = card.get_last_update()
        card.update_price(new_price)
        card.delete_old_prices()

        price_change = (new_price - last_price) / last_price
        if abs(price_change) < self.price_difference:
            price_change = 0
        else:
            price_change /= abs(price_change)

        return price_change

    def remove_card(self, card_idx):
        removed_card = self.interesting_cards.pop(card_idx)

        # If no cards to follow, destroy price updater thread
        if len(self.interesting_cards) == 0:
            self.thread_needs_to_be_alive = False
            self.price_updater_thread.join()
            self.price_updater_thread = None

        return removed_card
