from html2text import html2text
import requests
from bs4 import BeautifulSoup

DEFAULT_IMAGE = 'https://storage.googleapis.com/cbn-public/default-backgroud.jpg'


def extract(url):
    print('ProPublica extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')

    image_tag = soup.find('figure', {'class': 'lead-art'})
    if image_tag is None:
        image = DEFAULT_IMAGE
    else:
        image = image_tag.find('img')['src']

    description_tag = soup.find('h2', {'class': 'dek'})
    description = ''
    if description_tag is not None:
        description = description_tag.get_text()
    else:
        description_tag = soup.find('p', {'class': 'dek'})
    if description == '' and description_tag is not None:
        description = description_tag.get_text()

    content = soup.find('div', {'class': 'article-body'})
    [element.extract() for element in content.find_all('div', {'class': 'top-notes'})]

    if description == '':
        description = content.find('p').get_text()[0:150]

    for element in content(['script', 'style', 'aside']):
        element.decompose()

    content = html2text(content.decode()) + '\n\n*[Extracted from ProPublica](' + url + ' "source")*'
    return {
        'image': image,
        'content': content,
        'description': description
    }