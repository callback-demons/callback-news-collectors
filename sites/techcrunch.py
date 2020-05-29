from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('TechCrunch extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    article = soup.find('div', {'class': 'article-content'})
    image_tag = soup.find('img', {'class': 'article__featured-image'})
    if image_tag is None:
        image = soup.find('img')['src']
    else:
        image = image_tag['src']

    description = " ".join(article.get_text().strip().replace('\n', ' ').split())[0:150]
    content = html2text(article.decode()) + '\n\n*[Extracted from TechCrunch](' + url + ' "source")*'

    return {
        'image': image,
        'content': content,
        'description': description
    }