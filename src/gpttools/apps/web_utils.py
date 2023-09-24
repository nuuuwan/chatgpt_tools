from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from utils import Log

log = Log('web_utils')


def get_url_text(url):
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    driver.implicitly_wait(5)
    body_element = driver.find_element(By.TAG_NAME, 'body')
    text = body_element.text
    driver.quit()
    log.info(f'Extracted {len(text):,}B from {url}')
    return text
