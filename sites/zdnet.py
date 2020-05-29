from html2text import html2text
import requests
from bs4 import BeautifulSoup

DEFAULT_IMAGE = 'https://storage.googleapis.com/cbn-public/default-backgroud.jpg'


def extract(url):
    print('ZDNet extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    article = soup.find('article')
    image_parent = article.find('div', {'class': 'videoSlide'})
    if image_parent is None:
        image = DEFAULT_IMAGE
    else:
        image = image_parent.find('img')['src']

    content = article.find('div', {'class': 'storyBody'})
    description = " ".join(content.get_text().strip().replace('\n', ' ').split())[0:150]
    content = html2text(content.decode()) + '\n\n*[Extracted from ZDNet](' + url + ' "source")*'

    return {
        'image': image,
        'content': content,
        'description': description
    }