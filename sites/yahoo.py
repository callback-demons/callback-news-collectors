import json
from html2text import html2text
import requests
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
from bs4 import BeautifulSoup

URL = 'https://finance.yahoo.com/rss/tech/'
JSON_FILE = 'json/yahoo.json'


def get_json_from_rss():
    try:
        response = requests.get(URL)
        xml_data = fromstring(response.text)
        return json.dumps(bf.data(xml_data))
    except e:
        print('Error ', e)

def extract_article(url):
    print('extract from article')
    article = ''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tag = soup.find('article').find_all('p')
            article = ''.join(str(element) for element in tag)
        else:
            print('Error: ', response.status_code)
    except e:
        print('Error: ', e)
    finally:
        return article


def add_structure(item):
    if 'description' in item:
        description_md = html2text(item['description']['$'])
        item['description_md'] = {'$': description_md}
    else:
        description = extract_article(item['link']['$'])
        description_md = html2text(description)
        item['description'] = {'$': description}
        item['description_md'] = {'$': description_md}
    return item


def transform(json_data):
    data = json.loads(json_data)
    news = list(data['rss']['channel']['item'])
    return json.dumps(list(map(add_structure, news)))


def create_file(data):
    file = open(JSON_FILE, "w")
    file.write(data)
    file.close()


if __name__ == "__main__":
    data = get_json_from_rss()
    json_data = transform(data)
    create_file(json_data)
