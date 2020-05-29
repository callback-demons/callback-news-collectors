from html2text import html2text
import requests
from bs4 import BeautifulSoup


def extract(url):
    print('Engadget extract {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    article = soup.find('article', {'class': 'c-gray-1'})

    content_blocks = article.findAll('div', {'class': 'article-text'})
    contents = list()
    for element in content_blocks:
        p_tag = element.findAll('p')
        for item in p_tag:
            contents.append(item)

    contents_blocks = ''.join(element.decode() for element in contents)
    content = html2text(contents_blocks) + '\n\n*[Extracted from engadget](' + url + ' "source")*'

    tag = article.find('div')
    if tag.has_attr('id') and tag.attrs['id'] == 'page_body':
        description = contents[0].get_text()
        image = soup.find('img', {'class': 'stretch-img'})['src']
    else:
        description = article.find('div', {'class': 'mt-15'}).get_text()
        image = article.find('img', {'class': 'stretch-img'})['src']

    return {
        'image': image,
        'content': content,
        'description': description
    }