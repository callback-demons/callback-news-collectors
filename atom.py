from html2text import html2text
import requests
from bs4 import BeautifulSoup
import dateutil.parser
from sites.theconversation import extract as extractTheConversation


def get_data(feed_url, category_id, source_name, source_id, target, token):
    response = requests.get(feed_url)
    soup_atom = BeautifulSoup(response.text, 'lxml-xml')
    entries = soup_atom.find_all('entry')
    for entry in entries:
        title = entry.find('title').get_text()
        link = entry.find('link')['href']
        published = dateutil.parser.parse(entry.find('published').get_text())
        description = entry.find('summary').get_text()
        author = entry.find('author').find('name').get_text()
        source_data = {}
        date_posted = "{year}-{month}-{day}".format(
            year=published.year,
            month=published.month,
            day=published.day
        )

        if source_name == 'The Conversation':
            source_data = extractTheConversation(link)

        content = source_data['content']
        image = source_data['image']

        data = {
            'title': title,
            'link': link,
            "date_posted": date_posted,
            'description': description,
            'author': author,
            "content": content,
            "media": image,
            "category_id": category_id,
            "source_id": source_id,
            "published": True,
        }

        publish = requests.post(target, data=data, headers={'Authorization': 'Token {}'.format(token)})
        print(publish.text)
