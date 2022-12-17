import requests
from bs4 import BeautifulSoup

import json
from datetime import datetime
from .models import *

from celery import Celery

from celery import app, shared_task

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def TOI_scrapping():
    article_list=[]
    try:
        print("Scrapping starting")
        r=requests.get("https://timesofindia.indiatimes.com/rssfeedstopstories.cms")
        soup = BeautifulSoup(r.content, features='xml')
        articles=soup.find_all('item')
        for a in articles:
            title=a.find('title').text
            link=a.find('link').text
            published_wrong = a.find('pubDate').text
            # published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
            published = datetime.strptime(published_wrong, '%Y-%m-%dT%H:%M:%S%z')
            
            article={
                "title" : title,
                "link" : link,
                "published" : published,
                "source" : "TOI RSS"
            }
            article_list.append(article)
            print('Finished scraping the articles')

            return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


@shared_task(serializer='json')
def save_function(article_list):
    source = article_list[0]['source']
    new_count = 0

    error = True
    try: 
        latest_article = News.objects.filter(source=source).order_by('-id')[0]
        print(latest_article.published)
        print('var TestTest: ', latest_article, 'type: ', type(latest_article))
    except Exception as e:
        print('Exception at latest_article: ')
        print(e)
        error = False
        pass
    finally:     
        if error is not True:
            latest_article = None

    for article in article_list:

        if latest_article is None:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except Exception as e:
                print('failed at latest_article is none')
                print(e)
                break

        elif latest_article.published < article['published']:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_article.published < j[published]')
                break
        else:
            return print('news scraping failed')

    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')