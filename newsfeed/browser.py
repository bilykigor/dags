from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from random import sample
from pyvirtualdisplay import Display
import logging
import os

agents=[
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14'
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36'
    'Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0'
    'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36'
]

def get_browser_aws(browser=None):
    if browser is None:
        #display = Display(visible=0, size=(800, 600))
        #display.start()
        logging.info('Initialized virtual display..')
        
        options = Options()
        #options.add_argument("--headless")
        #options.add_argument("window-size=1400,1500")
        userAgent = sample(agents,1)[0]
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        #options.add_argument("--disable-accelerated-2d-canvas")
        #options.add_argument("--no-first-run")
        #options.add_argument("--no-zygote")
        #options.add_argument("--single-process")
        options.add_argument("enable-automation")
        options.add_argument("--dns-prefetch-disable")
        #options.add_argument("start-maximized"); # open Browser in maximized mode
        #options.add_argument("disable-infobars"); # disabling infobars
        #options.add_argument("--disable-extensions"); # disabling extensions
        #options.add_argument("--disable-gpu"); # applicable to windows os only
        #options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems

        
        #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option('useAutomationExtension', False)
        #options.add_argument('--disable-blink-features=AutomationControlled')

        browser = webdriver.Chrome(options=options)
    
    return browser

def get_browser(browser=None):
    if browser is None:
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chromeOptions.add_experimental_option("prefs",prefs)
        chromeOptions.add_argument("--incognito")
        #chromeOptions.add_argument("--headless")
        s=Service('/Users/ihor/Documents/Py/Yay/ChromeDriver')
        browser = webdriver.Chrome(options=chromeOptions,service=s)
        #browser.set_window_position(400, 0)
        wait = ui.WebDriverWait(browser,15)
        browser.implicitly_wait(3)
        
    return browser    

# def get_firefox_aws(browser=None):
#     if browser is None:
#         display = Display(visible=0, size=(800, 600))
#         display.start()
#         logging.info('Initialized virtual display..')

#         options = FirefoxOptions()
#         options.add_experimental_option('browser.download.folderList', 2)
#         options.add_experimental_option('browser.download.manager.showWhenStarting', False)

#         firefox_profile = webdriver.FirefoxProfile()
#         firefox_profile.set_preference('', 2)
#         firefox_profile.set_preference('', False)
#         #firefox_profile.set_preference('browser.download.dir', os.getcwd())
#         #firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

#         logging.info('Prepared firefox profile..')

#         browser = webdriver.Firefox(options=options)
#         logging.info('Initialized firefox browser..')

#     return browser