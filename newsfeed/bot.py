import sys
import logging
import requests

from newsfeed import config
import newsfeed.utils.db as db_utils

            
def send_news():
    logging.info('Reading data from DB')
    last_id = db_utils.select_last_id()
    news = db_utils.select_news(last_id)
    
    conn = db_utils.create_mysql_connector(config.db_news)
    db_utils.insert_records_to_table("variables",[{'name':'last_id','value':last_id}],'name', conn)
    
    if news.shape[0]>0:
        last_id = news.id.max()
        logging.info('Writing data to channel')
        
        failed=False
        for ix,row in news.iterrows():
            text = f"{row.title}\n{row.href}"
            query=f'https://api.telegram.org/bot{config.token}/sendMessage?chat_id={config.channel["id"]}&text={text}'
            res=requests.post(query)
            if res.status_code!=200:
                logging.error(f'Failed to send mgs \n {text}')
                logging.error(query)
                failed=True
        
        if failed:
            sys.exit(1) 
    
    return str(last_id)
            

if __name__ == "__main__":
    send_news()
