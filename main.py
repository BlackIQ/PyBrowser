import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import * 


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(10, 10, 1000, 800)
        
        self.setWindowTitle('Browser')
        self.setWindowIcon(QIcon('web.png'))
        
        self.createBrowser()
        
    def createBrowser(self):
        self.browser = Browser(self)
        self.setCentralWidget(self.browser)
        
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm close',
        "You are about to exit. Are you sure you want to continue?", QMessageBox.Yes | 
        QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
            

class Browser(QWidget):

    def __init__(self, parent):
        super(Browser, self).__init__(parent)
        
        _layout = QVBoxLayout(self)
        
        self.__controls()
        self.__layout()
        self.buttonStyle()
        _layout.addLayout(self.hbox)
        
        self.homePage = QUrl('https://www.google.com')
        self.web = QWebView()
        self.web.load(self.homePage)
        self.web.setMinimumHeight(qApp.primaryScreen().size().height()-160)
        _layout.addWidget(self.web)
        
        self.searchHistory = self.web.page().history()
        
        _layout.setAlignment(Qt.AlignTop)

    def historyButtonPush(self):
        self.popUp = QListWidget()
        
        for h in self.searchHistory.items():
            self.popUp.addItem(QListWidgetItem(h.title()))
            
        self.popUp.setWindowTitle('History')
        self.popUp.setMinimumSize(400, 400)
        
        self.popUp.itemActivated.connect(self.doubleClick)
        self.popUp.show()
        
        
    def doubleClick(self, item):
        for i in range(0, self.searchHistory.count()):
            if(self.searchHistory.itemAt(i).title() == item.text()):
                self.web.load(self.searchHistory.itemAt(i).originalUrl())
                break
        

    def forwardButtonPush(self):
        self.searchHistory.forward()
        
    def backButtonPush(self):
        self.searchHistory.back()

    def refreshButtonPush(self):
        self.web.reload()

    def homeButtonPush(self):
        self.web.load(self.homePage)

    def goButtonPush(self):
        tmp = self.addressBar.text()
        
        if(tmp == ''):
            return
        
        q = QUrl(tmp)
        if(q.scheme() == ""):
            q.setScheme("http");
            
        if(tmp.find('.') != -1 and tmp.find(' ') == -1):
            self.web.load(q)
                
        else:
            l = tmp.split()
            link = 'https://www.google.com/search?q=' + l[0]
            for i in range(1, len(l)):
                link += '+' + l[i]
            self.web.load(QUrl(link))
        
    def buttonStyle(self):
        buttonStyle = 'QPushButton{border:none;}'
        
        self.back.setIcon(QIcon('back.png'))
        self.back.setStyleSheet(buttonStyle); 
        self.back.setIconSize(QSize(25, 25));
        
        self.forward.setIcon(QIcon('forward.png'))
        self.forward.setStyleSheet(buttonStyle);
        self.forward.setIconSize(QSize(25, 25))
        
        self.home.setIcon(QIcon('home.png'))
        self.home.setStyleSheet(buttonStyle)
        self.home.setIconSize(QSize(22, 22))
        
        self.refresh.setIcon(QIcon('refresh.png'))
        self.refresh.setStyleSheet(buttonStyle)
        self.refresh.setIconSize(QSize(22, 22))
        
        self.bookmarks.setIcon(QIcon('bookmarks.png'))
        self.bookmarks.setStyleSheet(buttonStyle)
        self.bookmarks.setIconSize(QSize(22, 22))
        
        self.history.setIcon(QIcon('history.png'))
        self.history.setStyleSheet(buttonStyle)
        self.history.setIconSize(QSize(22, 22))
        
        self.settings.setIcon(QIcon('settings.png'))
        self.settings.setStyleSheet(buttonStyle)
        self.settings.setIconSize(QSize(22, 22))
        
        buttonStyle = 'QPushButton{border:none;}'
        self.go.setIcon(QIcon('search.png'))
        self.go.setStyleSheet(buttonStyle)
        self.go.setIconSize(QSize(22, 22))
        
    def __controls(self):
        self.back = QPushButton('')
        self.forward = QPushButton('')
        self.refresh = QPushButton('')
        self.home = QPushButton('')
        self.settings = QPushButton('settings')
        self.history = QPushButton('history')
        self.bookmarks = QPushButton('bookmarks')
        self.addressBar = QLineEdit()
        self.go = QPushButton('go')
        
        self.history.clicked.connect(self.historyButtonPush)
        self.forward.clicked.connect(self.forwardButtonPush)
        self.back.clicked.connect(self.backButtonPush)
        self.refresh.clicked.connect(self.refreshButtonPush)
        self.addressBar.editingFinished.connect(self.goButtonPush)
        self.go.clicked.connect(self.goButtonPush)
        self.home.clicked.connect(self.homeButtonPush)

    def __layout(self):
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.back)
        self.hbox.addWidget(self.forward)
        self.hbox.addWidget(self.refresh)
        self.hbox.addWidget(self.home)
        self.hbox.addWidget(self.addressBar)   
        self.hbox.addWidget(self.go)
        self.hbox.addWidget(self.bookmarks)
        self.hbox.addWidget(self.history)
        self.hbox.addWidget(self.settings) 
        

          

def main():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.showMaximized()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 
