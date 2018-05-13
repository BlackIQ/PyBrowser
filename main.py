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
            

class Browser(QGraphicsView):

    def __init__(self, parent):
        super(Browser, self).__init__(parent)
        
        self.page1 = Window(self)
        self.setScene(self.page1)
        

class Window(QGraphicsScene):
    
    def __init__(self, view):
        super(Window, self).__init__(view)
        
        _layout = QVBoxLayout(view)
        
        self.setBackgroundBrush(QBrush(QColor(230, 230, 230), Qt.SolidPattern))
        
        self.__controls()
        self.__layout()
        self.style()
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
            url = h.originalUrl()
            icon = QWebSettings.iconForUrl(url)
            self.popUp.addItem(QListWidgetItem(icon, h.title()))
            
        self.popUp.setWindowTitle('History')
        self.popUp.setMinimumSize(400, 400)
        
        self.popUp.itemActivated.connect(self.doubleClickHistory)
        self.popUp.show()
        
    def doubleClickHistory(self, item):
        for i in range(0, self.searchHistory.count()):
            if(self.searchHistory.itemAt(i).title() == item.text()):
                self.web.load(self.searchHistory.itemAt(i).originalUrl())
                break
        
    def bookmarksButtonPush(self):
        self.popUp = QListWidget()
        
        self.popUp.setWindowTitle('Bookmarks')
        self.popUp.setMinimumSize(400, 400)
        
        layout = QVBoxLayout()
        
        self.button = QPushButton('Delete mode')
        self.clicked = 0
        layout.addWidget(self.button)
        
        self.button.setFixedWidth(150)
        
        layout.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        
        self.popUp.setLayout(layout)
        
        file = open('bookmarks.txt', 'r')
        
        for line in file:
            list = line.split(';')
            url = QUrl(list[1])
            print url.toString()
            icon = QWebSettings.iconForUrl(url)
            self.popUp.addItem(QListWidgetItem(icon, list[0].strip()))
        
        self.button.clicked.connect(self.bookmarksButtonPushDelete)
        self.popUp.itemActivated.connect(self.doubleClickBookmark)
        
        self.popUp.show()
        
        file.close()
        
    def bookmarksButtonPushDelete(self):
        if(self.clicked == 0):
            self.clicked = 1
            self.button.setText('Back to bookmarks')
        else:
            self.clicked = 0
            self.button.setText('Delete mode')
        
        
    def doubleClickBookmark(self, item):
        file = open('bookmarks.txt', 'r')
        
        if(self.clicked == 0):
            for line in file:
                list = line.split(';')
                if(list[0].strip() == item.text().strip()):
                    q = QUrl(list[1].strip())
                    if(q.scheme() == ""):
                        q.setScheme("http")
                    self.web.load(q)
                    break
        else:
            lines = file.readlines()
            file.close()
            file = open('bookmarks.txt', 'w')
            for line in lines:
                list = line.split(';')
                if(list[0].strip() != item.text().strip()):
                    file.write(line)
            item.setHidden(True)
    
        file.close()
        


    def addBookmarkPush(self):
        self.popUp = QDialog()
        layout = QVBoxLayout()
        
        button = QPushButton('Done')
        self.add = QLineEdit()
        
        layout.addWidget(self.add)
        layout.addWidget(button)
        
        self.popUp.setLayout(layout)
        
        button.clicked.connect(self.addBokmark)
        
        self.popUp.setWindowTitle('Page Bookmarked')
        self.popUp.setMaximumSize(300, 200)
        
        self.popUp.show()

    def addBokmark(self):
        file = open('bookmarks.txt', 'a+')
        
        for line in file:
            list = line.split(';')
            if(list[0] == self.add.text()):
                return
        
        if(self.add.text().strip() != ''):
            file.write(self.add.text() + ';' + self.web.url().toString() + '\n')
            self.popUp.close()
            
        file.close()
        

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
            q.setScheme("http")
            
        if(tmp.find('.') != -1 and tmp.find(' ') == -1):
            self.web.load(q)
                
        else:
            l = tmp.split()
            link = 'https://www.google.com/search?q=' + l[0]
            for i in range(1, len(l)):
                link += '+' + l[i]
            self.web.load(QUrl(link))
        
    def style(self):
        buttonStyle = 'QPushButton{border:none;}' + 'QPushButton:hover{background-color: #dadada;}'
        
        self.back.setIcon(QIcon('back.png'))
        self.back.setStyleSheet(buttonStyle)
        self.back.setIconSize(QSize(25, 25))
        self.back.setToolTip('Go back one page')
        
        self.forward.setIcon(QIcon('forward.png'))
        self.forward.setStyleSheet(buttonStyle)
        self.forward.setIconSize(QSize(25, 25))
        self.forward.setToolTip('Go forward one page')
        
        self.refresh.setIcon(QIcon('refresh.png'))
        self.refresh.setStyleSheet(buttonStyle)
        self.refresh.setIconSize(QSize(22, 22))
        self.refresh.setToolTip('Reload current page')
        
        self.bookmarks.setIcon(QIcon('bookmarks.png'))
        self.bookmarks.setStyleSheet(buttonStyle)
        self.bookmarks.setIconSize(QSize(22, 22))
        self.bookmarks.setToolTip('Saved bookmarks')
        
        self.history.setIcon(QIcon('history.png'))
        self.history.setStyleSheet(buttonStyle)
        self.history.setIconSize(QSize(22, 22))
        self.history.setToolTip('View history')
        
        self.settings.setIcon(QIcon('settings.png'))
        self.settings.setStyleSheet(buttonStyle)
        self.settings.setIconSize(QSize(22, 22))
        self.settings.setToolTip('Settings')
        
        self.home.setIcon(QIcon('home.png'))
        self.home.setStyleSheet(buttonStyle)
        self.home.setIconSize(QSize(22, 22))
        self.home.setToolTip('Browser start page')
        
        self.go.setIcon(QIcon('search.png'))
        self.go.setStyleSheet(buttonStyle)
        self.go.setIconSize(QSize(20, 20))
        self.go.setToolTip('Go to location in the bar')
        
        self.addBookmark.setIcon(QIcon('star.png'))
        self.addBookmark.setStyleSheet(buttonStyle)
        self.addBookmark.setIconSize(QSize(20, 20))
        self.addBookmark.setToolTip('Bookmark this page')
        
        self.addressBar.setPlaceholderText('Search with Google or enter address')
        self.addressBar.addAction(QIcon('search.png'), QLineEdit.LeadingPosition)
        
    def __controls(self):
        self.back = QPushButton('')
        self.forward = QPushButton('')
        self.refresh = QPushButton('')
        self.home = QPushButton('')
        self.addressBar = QLineEdit()
        self.go = QPushButton('')
        self.addBookmark = QPushButton('')
        self.history = QPushButton('history')
        self.bookmarks = QPushButton('bookmarks')
        self.settings = QPushButton('settings')
        
        self.addBookmark.clicked.connect(self.addBookmarkPush)
        self.bookmarks.clicked.connect(self.bookmarksButtonPush)
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
        self.hbox.addSpacing(100)
        self.hbox.addWidget(self.addressBar)   
        self.hbox.addWidget(self.addBookmark)
        self.hbox.addWidget(self.go)
        self.hbox.addSpacing(100)
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
