from PyQt5.QtWidgets import *
from PyQt5 import uic

from crawler.web_crawler import WebCrawler
from crawler.popup_window import PopupWindowClass
from crawler.qthread_worker import QThreadWorker
from bs4 import BeautifulSoup

from PyQt5.QtCore import QCoreApplication, QMutex, QThread, QWaitCondition, pyqtSignal

import sys
import time
import json

class MainWindow(QMainWindow):
    gi = 0

    def __init__(self):
        super().__init__()

        uic.loadUi("login_form.ui", self)
        self.show()

        self.lineEdit_PW.setEchoMode(QLineEdit.Password)
        self.pushButton_LOGIN.clicked.connect(self.btn_event_login)
        self.pushButton_NOTI.clicked.connect(self.btn_event_noti)

        self.lineEdit_ID.setText('')
        self.lineEdit_PW.setText('')

        # Contents Update QThread Worker
        self.worker_contents = QThreadWorker(id='', password='', duration=4)
        self.worker_contents.signal.connect(self.worker_update_contents)

    def btn_event_login(self):
        self.line_id = self.lineEdit_ID.text()
        self.line_pw = self.lineEdit_PW.text()

        if self.line_id == '' or self.line_pw == '':
            QMessageBox.information(self, "알림", "ID 또는 PW를 입력하세요!")
        else:
            # 크롤링 초기화
            self.browser = WebCrawler()
            self.browser.login('', self.line_id, self.line_pw)
            self.event_form_change()

    def btn_event_noti(self, user_id, user_pw, url):
        main_window = PopupWindowClass(user_id, user_pw, url)
        main_window.show()


    def event_form_change(self):
        uic.loadUi("main_form.ui", self)
        self.show()
        self.lineEdit_TIME.setText(time.ctime())

        self.worker_contents.start()

    # Contents Update QThread Worker
    def worker_update_contents(self, item):

        dict_from_json = json.loads(item)

        print(dict_from_json['totalElements'])

        if MainWindow.gi == 0:
            MainWindow.gi = dict_from_json['totalElements']

            for line in dict_from_json['content']:
                self.listWidget_SQUARE.addItem(str(line['contents']))
        else:
            if dict_from_json['totalElements'] == MainWindow.gi:
                MainWindow.gi = dict_from_json['totalElements']
                self.btn_event_noti(self.line_id, self.line_pw, 408183)

                self.listWidget_SQUARE.clear()


                for line in dict_from_json['content']:
                    self.listWidget_SQUARE.addItem(str(line['contents']))






        # for line in html.select('div.cardTheme-item'):
        #     user_info = line.find('div', attrs={'class': 'user-info'})
        #     user_name = user_info. find('img')['alt']
        #     user_img = user_info.find('img')['src']
        #     user_date = user_info.find('span', attrs={'class': 'date'}).text
        #
        #     contents = line.find('div', attrs={'class': 'feed-desc'}).text
        #     self.listWidget_SQUARE.addItem(str(contents))
        #     print(contents)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    sys.exit(app.exec_())
