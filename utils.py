import urllib.request
from urllib.error import HTTPError,URLError

def download_html(page_url):
	try:
		response = urllib.request.urlopen(page_url)
	except (HTTPError, URLError) as error:
		logging.error(" Data of \"%s\" not retrieved because %s\n", page_url, error)
	except ValueError:
		logging.error(" Unknown url type\n")

	page_content = response.read().decode("utf-8")
	return page_content