users = {}

class User:
	user_id = -1
	thread_needs_to_be_alive = True
	price_updater_thread = None
	retrieved_cards = []
	interesting_cards = []
	timeout_seconds = 3600 # 1 hour

	def __init__(self, new_id):
		if new_id <= 0:
			raise ValueError("User Id cannot be zero or negative")
		self.user_id = new_id

	def get_interesting_cards(self):
		return self.interesting_cards

	def add_card(self, new_card):
		self.interesting_cards.append(new_card)
		self.interesting_cards = list(set(self.interesting_cards))

	def remove_card(self, card_to_remove):
		self.interesting_cards.remove(card_to_remove)

	def get_timeout(self):
		return self.timeout_seconds
