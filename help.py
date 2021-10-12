def help_command(update, context):
	help_message = "I comandi disponibili sono:\n/start\n/help\n/html"
	context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)