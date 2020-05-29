from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('Shareable extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    article = soup.find('div', {'class': 'entry-content'})
    image = soup.find('img', {'class': 'attachment-large'})['src']
    tag_p = article.findAll('p')
    description = ''.join(str(element.get_text()) for element in tag_p)[0:150]
    content = html2text(article.decode()) + '\n\n*[Extracted from Shareable](' + url + ' "source")*'
    return {
        'image': image,
        'content': content,
        'description': description
    }