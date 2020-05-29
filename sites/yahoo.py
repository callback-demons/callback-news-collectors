from html2text import html2text
import requests
from bs4 import BeautifulSoup
import re

DEFAULT_IMAGE = 'https://storage.googleapis.com/cbn-public/default-backgroud.jpg'


def extract(url, item):
    print('Yahoo Finance News / Tech extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')

    media_content = item.find('media:content')
    if media_content is None:
        image = DEFAULT_IMAGE
    else:
        medias = re.split(r'http://|https://', media_content['url'])
        while "" in medias:
            medias.remove("")
        if len(medias) > 1:
            image = 'https://' + medias[1]
        else:
            image = 'https://' + medias[0]

    author_tag = soup.find('div', {'class': 'auth-attr'})
    if author_tag.find('div', {"class": 'author-name'}) is not None:
        author = author_tag.find('div', {"class": 'author-name'}).get_text()
    elif author_tag.find('div', {"class": 'auth-prov-soc'}).find('span', {'class': 'provider-link'}) is not None:
        author = author_tag.find('div', {"class": 'auth-prov-soc'}).find('span', {'class': 'provider-link'}).get_text()
    else:
        author = author_tag.find('a').get_text()

    article = soup.find('article')
    for element in article(['figure', 'br']):
        element.decompose()

    for element in article.find_all():
        if len(element.get_text(strip=True)) == 0:
            element.extract()

    description = article.find('p').get_text()[0:150]
    content = html2text(article.decode()) + '\n\n*[Extracted from Yahoo Finance News / Tech](' + url + ' "source")*'

    return {
        'image': image,
        'content': content,
        'author': author,
        'description': description
    }
