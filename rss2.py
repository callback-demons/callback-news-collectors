import re
from html2text import html2text
import requests
from bs4 import BeautifulSoup
import dateutil.parser
from sites.xakatamx import extract as extractXakataMX
from sites.zdnet import extract as extractZDNet
from sites.engadget import extract as extractEngadget
from sites.fayerwayer import extract as extractFayerWayer
from sites.propublica import extract as extractProPublica
from sites.shareable import extract as extractShareable
from sites.singularityhub import extract as extractSingularityHub
from sites.yahoo import extract as extractYahoo
from sites.techcrunch import extract as extractTechCrunch
from sites.torrentfreak import extract as extractTorrentFreak

REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def get_data(feed_url, category_id, source_name, source_id, target, token):
    response = requests.get(feed_url)
    soup_rss = BeautifulSoup(response.text, 'lxml-xml')
    items = soup_rss.find_all('item')
    source_data = {}
    for item in items:
        if re.match(REGEX, item.find('link').get_text()) is not None:
            pubdate = dateutil.parser.parse(item.find('pubDate').get_text())
            date_posted = "{year}-{month}-{day}".format(
                year=pubdate.year,
                month=pubdate.month,
                day=pubdate.day
            )
            author = ''

            if source_name == 'Xatakamx' or source_name == 'Engadget' or \
                    source_name == 'Propublica' or source_name == 'Fayerwayer' or \
                    source_name == 'Shareable' or source_name == 'Singularity Hub' or \
                    source_name == 'Techcrunch' or source_name == 'TorrentFreak':
                author = item.find('dc:creator').get_text()

            if source_name == 'Xatakamx':
                source_data = extractXakataMX(item.find('link').get_text())
            if source_name == 'Zdnet':
                author = item.find('media:credit').get_text()
                source_data = extractZDNet(item.find('link').get_text())
            if source_name == 'Engadget':
                source_data = extractEngadget(item.find('link').get_text())
            if source_name == 'Fayerwayer':
                source_data = extractFayerWayer(item.find('link').get_text())
            if source_name == 'Propublica':
                source_data = extractProPublica(item.find('link').get_text())
            if source_name == 'Shareable':
                source_data = extractShareable(item.find('link').get_text())
            if source_name == 'Singularity Hub':
                source_data = extractSingularityHub(item.find('link').get_text())
            if source_name == 'Yahoo Finance News / Tech':
                source_data = extractYahoo(item.find('link').get_text(), item)
                author = source_data['author']
            if source_name == 'Techcrunch':
                source_data = extractTechCrunch(item.find('link').get_text())
            if source_name == 'TorrentFreak':
                source_data = extractTorrentFreak(item.find('link').get_text())

            content = source_data['content']
            image = source_data['image']
            description = source_data['description']

            data = {
                "title": item.find('title').get_text(),
                "author": author,
                "description": description,
                "content": content,
                "date_posted": date_posted,
                "user_id": "1",
                "media": image,
                "category_id": category_id,
                "source_id": source_id,
                "published": True,
            }
            publish = requests.post(target, data=data, headers={'Authorization': 'Token {}'.format(token)})
            print(publish.text)
