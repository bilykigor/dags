from newsfeed.browser import get_browser_aws
from selenium.webdriver.common.by import By
from newsfeed import config
import newsfeed.utils.db as db_utils
import logging
import sys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


def wait_on_capcha(browser):
    while True:
        captures1=browser.find_elements(By.CLASS_NAME,'CheckboxCaptcha') #CheckboxCaptcha-Checkbox
        captures2=browser.find_elements(By.CLASS_NAME,'AdvancedCaptcha')

        if len(captures1)+len(captures2)>0:
            logging.info(f'Captcha found')
            sleep(30)
        else: 
            return

    
def get_news_yandex(regions):
    browser = None
    failed = False
    
    for region in regions:
        source=f'https://yandex.ru/news/region/{region}'
        logging.info(f'Browsing to {source}')

        if browser is None:
            browser=get_browser_aws(browser)
        else:
            try:
                browser.find_element(By.CLASS_NAME,'mg-collapsing-items__item-inner').click()
                wait_on_capcha(browser)
                sleep(5)
                options = browser.find_elements(By.CLASS_NAME,'news-regions__table-link')
                options = [o for o in options if o.get_attribute('href')==f'https://yandex.ru/news/region/{region}']
                if len(options)==0:
                    logging.error(f'Failed to find link to {region}')
                    browser = None
                    sleep(5)
                    continue
                action =  ActionChains(browser)
                action.move_to_element(options[0]).click().perform()
                #option.click()
                wait_on_capcha(browser)
                sleep(5)
            except Exception as e:
                logging.error('Failed to open browser')
                logging.error(e)
                browser.quit()
                browser = None
                sleep(5)
                continue

        try:
            browser.get(source)
            wait_on_capcha(browser)
            sleep(5)
        except Exception as e:
            logging.error('Failed to open browser')
            logging.error(e)
            browser.quit()
            browser = None
            sleep(10)
            continue

        news = browser.find_elements(By.CLASS_NAME,'mg-card__inner')#mg-card__title
        logging.info(f'Reading {len(news)} news from main page {source}')
        if len(news)>0:
            action =  ActionChains(browser)
            action.move_to_element(news[0]).perform()
            
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
            
        
            conn = db_utils.create_mysql_connector(config.db_news)
            db_utils.insert_records_to_table("news",records,'title', conn)
            sleep(5)
        else:
            logging.warning(f'Failed to read news from {source}')
            browser.quit()
            browser = None
            failed=True
            sleep(5)
    
    if browser:
        browser.quit()

    if failed:        
        sys.exit(1)

        
        
