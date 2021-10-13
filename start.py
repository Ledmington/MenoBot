def start_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello, welcome to MenoBot.")
