from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import Log

log = Log('web_utils')


def get_url_text(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(5)
    body_element = driver.find_element(By.TAG_NAME, 'body')
    text = body_element.text
    driver.quit()
    log.debug(f'Extracted {len(text):,}B from {url}')
    return text
