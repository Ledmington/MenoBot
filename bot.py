from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import logging
import urllib.request
from urllib.error import HTTPError,URLError
from socket import timeout
import re

forbidden_extension = [".png", ".PNG", ".svg", ".jpg", ".JPG", ".jpeg", ".bmp", ".ico", ".gif"]
links_regex = re.compile("((https?:)?\/\/(\w|\d|\.|\/|\-|\?|\=|\&|\;)*)")

def parse_links(html_code):
	links = links_regex.findall(html_code)
	links = [l[0] for l in links]

	# Removing links to images
	for l in links[:]:
		for extension in forbidden_extension:
			if extension in l:
				links.remove(l)
				break

	# Removing trailing '/'
	links_copy = links.copy()
	for l in range(0, len(links)-1):
		if(links[l].endswith("/")):
			links_copy[l] = links_copy[l][:-1]
	links = links_copy
	
	# Removing leading "//"
	links_copy = links.copy()
	for l in range(0, len(links)-1):
		if(links[l].startswith("//")):
			links_copy[l] = "http:"+links_copy[l]
		elif "//" not in links[l]:
			links_copy[l] = "http://"+links_copy[l]
	links = links_copy
	links = list(set(links))

	return links

def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, benvenuto su MenoBot 0.1")

def help(update, context):
	help_message = "I comandi disponibili sono:\n/start\n/help\n/html"
	context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def html(update, context):
	main_page_url = "https://www.cardmarket.com/it/YuGiOh"
	cards_list_url = "https://www.cardmarket.com/it/YuGiOh/Products/Singles"

	try:
		response = urllib.request.urlopen(cards_list_url)
	except (HTTPError, URLError) as error:
		logging.error(" Data of \"%s\" not retrieved because %s\n", cards_list_url, error)
	except ValueError:
		logging.error(" Unknown url type\n")

	page_content = response.read().decode("utf-8")
	links = parse_links(page_content)
	context.bot.send_message(chat_id=update.effective_chat.id, text=links)

def main() -> None:
	# Reading token
	with open("token", "r") as token_file:
		mytoken = token_file.read()

	updater = Updater(token=mytoken, use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)

	help_handler = CommandHandler('help', help)
	dispatcher.add_handler(help_handler)

	html_handler = CommandHandler('html', html)
	dispatcher.add_handler(html_handler)

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()