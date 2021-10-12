import urllib.request
from urllib.error import HTTPError,URLError
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

def get_cards_list(update, context):
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