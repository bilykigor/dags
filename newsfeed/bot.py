from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel
import sys
import socks
import logging
from newsfeed import config
import newsfeed.utils.db as db_utils
import asyncio
from time import sleep


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

    
def find_channel(client, channel_id, channel_name=None):
    channel_found=False
    for d in client.iter_dialogs():
        if d.name == channel_name or d.entity.id == channel_id:
            #output_channel=InputChannel(d.entity.id, d.entity.access_hash)
            logging.info('Channel found')
            channel_found=True
            break
    
    return channel_found
            
def send_news():
    client = TelegramClient(config.telegram["session_name"], 
                            config.telegram["api_id"], 
                            config.telegram["api_hash"])
                            #proxy=(socks.SOCKS5, "185.157.121.164", 8080, True))
    client.start()

    channel_found = find_channel(client,config.channel["id"])
    
    if not channel_found:
        logging.error('Channel not found')
        return
    
    async def send_news():
        last_id = None
        logging.info('Reading data from DB')
        news = db_utils.select_news(last_id)
        
        if news.shape[0]>0:
            last_id = news.id.max()
            logging.info('Writing data to channel')
            
            for ix,row in news.iterrows():
                msg = f"{row.title}\n{row.href}"
                await client.send_message(config.channel["id"], msg)
    
    client.loop.run_until_complete(send_news())
    client.disconnect()
    

if __name__ == "__main__":
    send_news()
