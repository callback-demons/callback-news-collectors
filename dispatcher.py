import json
import requests
from rss2 import get_data as rss_data
from atom import get_data as atom_data

TOKEN = ''
news_url = 'https://api.callback-news.com'

def get_categories():
    url = news_url + '/categories'
    response = requests.get(url)
    return response.json()


def get_sources():
    url = news_url + '/sources'
    response = requests.get(url)
    return response.json()


def dispatch(sources, categories):
    index = 0
    for source in sources:
        category = categories[index % len(categories)]
        print(source['feed_url'])
        if source['feed_type'] == 'rss2':
            rss_data(
                feed_url=source['feed_url'],
                category_id=category['id'],
                source_id=source['id'],
                source_name=source['name'],
                target=news_url + '/news-publish',
                token=TOKEN
            )
        if source['feed_type'] == 'atom':
            atom_data(
                feed_url=source['feed_url'],
                category_id=category['id'],
                source_id=source['id'],
                source_name=source['name'],
                target=news_url + '/news-publish',
                token=TOKEN
            )
        index += 1


if __name__ == "__main__":
    categories = get_categories()
    sources = get_sources()
    dispatch(sources, categories)
