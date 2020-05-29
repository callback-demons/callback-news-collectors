from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('The Conversation extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')

    image = soup.find('figure', {'class': ['content-lead-image', 'magazine']}).find('img')['src']

    entry = soup.find('div', {'class': 'entry-content'})
    content = html2text(entry.decode()) + '\n\n*[Extracted from The Conversation](' + url + ' "source")*'

    return {
        'image': image,
        'content': content
    }