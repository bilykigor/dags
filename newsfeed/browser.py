from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

def get_browser_aws(browser=None):
    if browser is None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("window-size=1400,1500")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        
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
