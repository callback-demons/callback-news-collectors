import json
from html2text import html2text
import requests
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf

URL = 'http://feeds.feedburner.com/fayerwayer?format=xml'
JSON_FILE = 'json/fayerwayer.json'


def get_json_from_rss():
    try:
        response = requests.get(URL)
        xml_data = fromstring(response.text)
        return json.dumps(bf.data(xml_data))
    except e:
        print('Error ', e)


def add_structure(item):
    if 'description' in item:
        description_md = html2text(item['description']['$'])
        item['description_md'] = {'$': description_md}
    else:
        print(item)
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
