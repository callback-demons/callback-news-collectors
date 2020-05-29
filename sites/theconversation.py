import json
from html2text import html2text
import requests
from bs4 import BeautifulSoup

URL = 'https://theconversation.com/global/technology/articles.atom'
JSON_FILE = 'json/theconversation.json'


def get_json_from_rss():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'lxml')
        entries = soup.find_all('entry')
        data = []
        for entry in entries:
            data.append({
                'title': entry.find('title').get_text(),
                'link': entry.find('link')['href'],
                'pubDate': entry.find('published').get_text(),
                'description': entry.find('content').get_text(),
                'author': entry.find('author').get_text(),
            })
        return json.dumps(data)
    except e:
        print('Error ', e)


def add_structure(item):
    if 'description' in item:
        description_md = html2text(item['description'])
        item['description_md'] = description_md
    else:
        print(item)
    return item


def transform(json_data):
    news = json.loads(json_data)
    return json.dumps(list(map(add_structure, news)))


def create_file(data):
    file = open(JSON_FILE, "w")
    file.write(data)
    file.close()


if __name__ == "__main__":
    data = get_json_from_rss()
    json_data = transform(data)
    create_file(json_data)
