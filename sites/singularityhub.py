from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('SingularityHub extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    article = soup.find('div', {'class': 'td-post-content'})
    image_tag = soup.find('img', {'class': 'td-backstretch'})
    if image_tag is not None:
        image = image_tag['src']
    else:
        image_parent = soup.find('div', {'class': 'td-post-featured-image'})
        image = image_parent.find('img')['src']

    [element.extract() for element in article.find_all('div', {'class': 'addthis_tool'})]
    [element.extract() for element in article.find_all('iframe')]

    description = article.find('p').get_text()
    content = html2text(article.decode()) + '\n\n*[Extracted from SingularityHub](' + url + ' "source")*'

    return {
        'image': image,
        'content': content,
        'description': description
    }