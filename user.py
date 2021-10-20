import threading
import time
import utils

users = {}

class User:
	user_id = -1
	thread_needs_to_be_alive = True
	price_updater_thread = None
	retrieved_cards = []
	interesting_cards = []
	price_difference = 0.01 # 1%
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
			self.thread_needs_to_be_alive = True
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

	def update_all_prices(self, update, context):
		message = ""
		for c in self.interesting_cards:
			price_changed = self.force_update_price(c)
			if price_changed:
				message += "<a href=\"" + c.get_url() + "\"><b>" + c.get_name() + "</b></a> has changed price to " + str(c.get_last_update()).replace(".", ",") + " €\n"

		if message is not None:
			context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML", disable_web_page_preview=True)

	def force_update_price(self, card):
		new_price = utils.download_price(card.get_url())
		last_price = card.get_last_update()
		card.update_price(new_price)

		return abs(new_price - last_price) / min(new_price, last_price) >= self.price_difference

	def remove_card(self, card_idx):
		removed_card = self.interesting_cards.pop(card_idx)

		# If no cards to follow, destroy price updater thread
		if(len(self.interesting_cards) == 0):
			self.thread_needs_to_be_alive = False
			self.price_updater_thread.join()
			self.price_updater_thread = None

		return removed_card

	def get_timeout(self):
		return self.timeout_seconds