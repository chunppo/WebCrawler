from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

# 웹크롤링 클래스
class WebCrawler:
    CONST_AGENT_ID = 'phantomjs.page.settings.userAgent'
    CONST_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    def __init__(self, display_flag=False):
        # selenium 브라우져 Aget를 설정한다.
        d_cap = dict(DesiredCapabilities.PHANTOMJS)
        d_cap[WebCrawler.CONST_AGENT_ID] = (
            WebCrawler.CONST_AGENT
        )

        # Phantom 모드로 동작시킬지 구분함
        if display_flag:
            self.browser = webdriver.Chrome(desired_capabilities=d_cap)
        else:
            self.browser = webdriver.PhantomJS(desired_capabilities=d_cap)
        self.browser.implicitly_wait(3)

    def login(self, login_url, id, pw):
        self.browser.get(login_url)

        self.browser.find_element_by_name('username').send_keys(id)
        self.browser.find_element_by_name('password').send_keys(pw)
        time.sleep(2)

        self.browser.find_element_by_css_selector('.btn-submit').click()

        try:
            WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-submit')))
            print('Click is ready!')
        except Exception:
            print('Click took too much time!')

    def get_browser_html(self, page_url):
        self.browser.get(page_url)

        try:
            WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'nano-page-square-list')))
            print("Page is ready!")
        except Exception:
            print("Loading took too much time!")

        page_lxml = BeautifulSoup(self.browser.page_source, 'lxml')

        return page_lxml

if __name__ == '__main__':
    browser = WebCrawler()
    browser.login('URL', 'ID', 'PASSWORD')
    html = browser.get_browser_html('VIEW_URL')

