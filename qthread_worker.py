from PyQt5.QtCore import QThread, pyqtSignal
from crawler.web_crawler import WebCrawler
from bs4 import BeautifulSoup

import time
import json

# QThread Common Worker
class QThreadWorker(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent=None, id=None, password=None, duration=1):
        QThread.__init__(self, parent)
        self.id = id
        self.password = password
        self.duration = duration

    def run(self):
        browser = WebCrawler()
        browser.login('', self.id, self.password)

        while True:
            # html = browser.get_browser_html('')

            html = browser.get_browser_json('')


            soup = BeautifulSoup(html, 'lxml').text


            self.signal.emit(str(soup))
            time.sleep(self.duration)
