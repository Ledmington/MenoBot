class User:
	user_id = -1
	thread_needs_to_be_alive = True
	price_updater_thread = None
	interesting_cards = []
	timeout_seconds = 600

	def __init__(self, new_id):
		if new_id <= 0:
			raise ValueError("User Id cannot be zero or negative")
		self.user_id = new_id

	def get_cards(self):
		return self.interesting_cards

	def add_card(self, new_card):
		interesting_cards.append(new_card)

	def remove_card(self, card_to_remove):
		interesting_cards.remove(card_to_remove)
