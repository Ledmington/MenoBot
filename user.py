import threading
import time

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

	def add_card(self, new_card, update, context):
		self.interesting_cards.append(new_card)
		self.interesting_cards = list(set(self.interesting_cards))

		if self.price_updater_thread == None:
			self.price_updater_thread = threading.Thread(target=self.__updater_thread_function__, args=(update, context,))
			self.price_updater_thread.start()

	def __updater_thread_function__(self, update, context,):
		time_passed = 0
		while self.thread_needs_to_be_alive == True:
			if(time_passed >= self.timeout_seconds):
				time_passed = 0
				self.update_all_prices(update, context)
			time.sleep(10)
			time_passed += 10

	def remove_card(self, card_to_remove):
		self.interesting_cards.remove(card_to_remove)

	def get_timeout(self):
		return self.timeout_seconds