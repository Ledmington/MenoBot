import datetime

class Card:
	# Full name
	name = ""

	# Full url to reach the card
	url = ""

	# List of tuples (price, datetime) of last 30 days
	prices = []

	def __init__(self, card_name, card_url):
		self.name = card_name
		self.url = card_url
		self.prices.append((float(0), datetime.datetime.now()))

	def get_name(self):
		return self.name

	def get_url(self):
		return self.url

	def get_prices(self):
		return self.prices

	def get_last_update(self):
		return prices[-1][1]

	def update_price(self, new_price):
		if new_price < 0:
			raise ValueError("Price can't be negative")
		self.prices.append((float(new_price), datetime.datetime.now()))