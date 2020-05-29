from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('TorrentFreak extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    image = soup.find('img')['src']
    description = " ".join(soup.find('p', {'class': 'article__excerpt'}).get_text().strip().replace('\n', ' ').split())
    content = soup.find('div', {'class': 'article__body'})
    content = html2text(content.decode()) + '\n\n*[Extracted from TorrentFreak](' + url + ' "source")*'
    return {
        'image': image,
        'content': content,
        'description': description
    }