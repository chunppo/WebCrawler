from PyQt5 import QtCore, QtGui, QtWidgets
from crawler.web_crawler import WebCrawler

class PopupWindowClass(QtWidgets.QWidget):
    popuphidden = QtCore.pyqtSignal()

    def __init__(self, user_id, user_pw, url):
        super(PopupWindowClass, self).__init__()
        self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.setMinimumSize(QtCore.QSize(300, 100))
        self.animation = QtCore.QPropertyAnimation(self, b"windowOpacity", self)
        self.animation.finished.connect(self.hide)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hideAnimation)
        self.setupUi()
        self.setPopupText('message')

        self.user_id = user_id
        self.user_pw = user_pw
        self.url = url

    def setupUi(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        appearance = self.palette()
        appearance.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                            QtGui.QColor("green"))
        self.setPalette(appearance)
    def setPopupText(self, text):
        self.label.setText(text)
        self.label.adjustSize()
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

            browser = WebCrawler(True)
            browser.login('', self.user_id, self.user_pw)
            browser.get_browser_html('')
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
    def show(self):
        self.setWindowOpacity(0.0)
        self.animation.setDuration(1500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        QtWidgets.QWidget.show(self)
        self.animation.start()
        self.timer.start(5000)

        self.move2RightBottomCorner(self)

    def hideAnimation(self):
        self.timer.stop()
        self.animation.setDuration(1500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()
    def hide(self):
        if self.windowOpacity() == 0:
            QtWidgets.QWidget.hide(self)
            self.popuphidden.emit()

    def move2RightBottomCorner(self, win):
        try:
            screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
            screen_size = (screen_geometry.width(), screen_geometry.height())
            win_size = (win.frameSize().width(), win.frameSize().height())
            x = screen_size[0] - win_size[0] - 10
            y = screen_size[1] - win_size[1] - 10
            win.move(x, y)
        except Exception as e:
            print (e)
