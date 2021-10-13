import utils

interesting_cards = set()

def get_most_wanted_cards(update, context):
	cards_list_url = "https://www.cardmarket.com/en/YuGiOh/Products/Singles"
	base_url = "https://www.cardmarket.com"

	page_content = utils.download_html(cards_list_url)

	cards = utils.parse_cards(page_content)

	message = ""
	for c in cards:
		message = message + "<a href=\"" + base_url + c[1] + "\">" + c[0] + "</a>\n"
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

def get_my_cards(update, context):
	if len(interesting_cards) == 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You are following 0 cards.")
		return