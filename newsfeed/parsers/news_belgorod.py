from newsfeed.browser import get_browser_aws
from selenium.webdriver.common.by import By
from newsfeed import config
import newsfeed.utils.db as db_utils
import logging
import sys

def get_news_belgorod():
    browser=get_browser_aws()
    
    source='https://yandex.ru/news/region/belgorod'
    browser.get(source)
    browser.implicitly_wait(5)
    
    news = browser.find_elements(By.CLASS_NAME,'mg-card__title')
    logging.info(f'Reading {len(news)} news from main page')
    records=[]
    for li in news:
        record={}
        href = li.find_element(By.TAG_NAME,'a').get_attribute('href')
        href = href.split('?lang')[0]
        record['href'] = href
        record['title'] = li.text
        record['source'] = source
        records.append(record)
        logging.info(record['title'])
        
    if len(records)>0:
        conn = db_utils.create_mysql_connector(config.db_news)
        db_utils.insert_records_to_table("news",records,'title', conn)
        return len(records)
    else:
        logging.warning(f'Failed to read news from {source}')
        sys.exit(1)
        
