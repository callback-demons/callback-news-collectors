from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('XakataMX extract {}'.format(url))
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html5lib')
    soup.prettify('utf-8')
    article = soup.find('article', {'class': 'single-post'})
    image = article.find('div', {'class': 'thumbnail'}).find('img')['src']
    content = article.find('div', {'class': 'content-note'})
    description = article.find('div', {'class': 'description'}).find('h2').get_text()
    content = html2text(content.decode()) + '\n\n*[Extracted from FayerWayer](' + url + ' "source")*'
    return {
        'image': image,
        'content': content,
        'description': description
    }