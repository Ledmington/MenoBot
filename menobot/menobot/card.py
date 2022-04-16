import datetime


class Card:
    # Full name
    __name = ""

    # Full url to reach the card
    __url = ""

    # List of tuples (price, datetime) of last 30 days
    __prices = []

    def __init__(self, card_name, card_url):
        self.__name = card_name
        self.__url = card_url
        self.__prices = [(float(1e-6), datetime.datetime.now())]

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_prices(self):
        return self.__prices

    def get_last_update(self):
        return self.__prices[-1][0]

    def update_price(self, new_price):
        if new_price < 0:
            raise ValueError("Price can't be negative")
        self.__prices.append((float(new_price), datetime.datetime.now()))

    def delete_old_prices(self):
        oldest = list(
            filter(
                lambda price: (datetime.datetime.now() - price[1]).days >= 30,
                self.__prices,
            )
        )
        if len(oldest) > 0:
            for old in oldest:
                self.__prices.remove(old)
