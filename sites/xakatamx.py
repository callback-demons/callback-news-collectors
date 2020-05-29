from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('XakataMX extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    article = soup.find('article')
    image_parent = soup.find('div', {'class': ['article-asset-image', 'article-featured-cover']})
    image = image_parent.find('img')['src']
    content = article.find('div', {'class': 'blob'})
    description = " ".join(content.get_text().strip().replace('\n', ' ').split())[0:150]
    content = html2text(content.decode()) + '\n\n*[Extracted from Xakata](' + url + ' "source")*'
    return {
        'image': image,
        'content': content,
        'description': description
    }