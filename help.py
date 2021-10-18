def help_command(update, context):
	help_message = """Available commands:
					  <b>help</b> - Show a list of available commands
					  <b>list_most_wanted_cards</b> - Show most wanted cards on CardMarket
					  <b>list_my_cards</b> - Show the cards you are following
					  <b>add_card</b> card - Start following a card
					  <b>remove_card</b> card_number - Stop following a card
					  <b>search</b> card - Looks for a card on CardMarket
					  <b>update_price</b> card_number - Forces price update of a card
					  <b>update_prices</b> - Forces price update of all cards
					  <b>set_timeout</b> timeout - Changes time to wait between price updates"""
	context.bot.send_message(chat_id=update.effective_chat.id, text=help_message, parse_mode="HTML")