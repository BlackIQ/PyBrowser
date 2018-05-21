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
        
        tb = self.addToolBar("File")
        tb.setMovable(False)
        backAction = QAction(QIcon('back.png'), 'Back', self)
        backAction.setShortcut('Ctrl+Q')
        backAction.triggered.connect(self.browser.page.backButtonPush)

        forwardAction = QAction(QIcon('forward.png'), 'Forward', self)
        forwardAction.setShortcut('Ctrl+Q')
        forwardAction.triggered.connect(self.browser.page.forwardButtonPush)

        refreshAction = QAction(QIcon('refresh.png'), 'Refresh', self)
        refreshAction.setShortcut('Ctrl+Q')
        refreshAction.triggered.connect(self.browser.page.refreshButtonPush)

        homeAction = QAction(QIcon('home.png'), 'Home', self)
        homeAction.setShortcut('Ctrl+Q')
        homeAction.triggered.connect(self.browser.page.homeButtonPush)
        
        addressBar = QLineEdit()
        addressBar.setPlaceholderText('Search with Google or enter address')
        addressBar.editingFinished.connect(lambda: self.browser.page.goButtonPush(addressBar.text()))
        
        goAction = QAction(QIcon('search.png'), 'Go', self)
        goAction.setShortcut('Ctrl+Q')
        goAction.triggered.connect(lambda: self.browser.page.goButtonPush(addressBar.text()))
        
                    
        bookmarkAction = QAction(QIcon('star.png'), 'Add bookmark', self)
        bookmarkAction.setShortcut('Ctrl+Q')
        bookmarkAction.triggered.connect(self.browser.page.addBookmarkPush)
            
        historyAction = QAction(QIcon('history.png'), 'History', self)
        historyAction.setShortcut('Ctrl+Q')
        historyAction.triggered.connect(self.browser.page.historyButtonPush)
            
        bookmarksAction = QAction(QIcon('bookmarks.png'), 'Bookmarks', self)
        bookmarksAction.setShortcut('Ctrl+Q')
        bookmarksAction.triggered.connect(self.browser.page.bookmarksButtonPush)
            
        settingsAction = QAction(QIcon('settings.png'), 'Settings', self)
        settingsAction.setShortcut('Ctrl+Q')
        settingsAction.triggered.connect(self.browser.page.refreshButtonPush)
        
        
        
        tb.addAction(backAction)
        tb.addAction(forwardAction)
        tb.addAction(refreshAction)
        tb.addAction(homeAction)
        tb.addWidget(addressBar)
        tb.addAction(goAction)
        tb.addAction(bookmarkAction)
        tb.addAction(historyAction)
        tb.addAction(bookmarksAction)
        tb.addAction(settingsAction)
        
        
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
        self.page = Window(self)
        self.setScene(self.page)
        

class Window(QGraphicsScene):
    
    def __init__(self, view):
        super(Window, self).__init__(view)
        
        _layout = QVBoxLayout(view)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
       
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")


        self.setBackgroundBrush(QBrush(QColor(230, 230, 230), Qt.SolidPattern))

        self.tab1.layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1.layout)

        self.homePage = QUrl('https://www.google.com')
        self.web = QWebView()
        self.web.load(self.homePage)
        self.web.setMinimumHeight(qApp.primaryScreen().size().height()-160)
        
        
        self.tab1.layout.addWidget(self.web)
        
        self.searchHistory = self.web.page().history()
        

        self.tab1.layout.setAlignment(Qt.AlignTop)
        _layout.addWidget(self.tabs)
        
# History Button
    def historyButtonPush(self):
        self.popUp = QListWidget()
        
        for h in self.searchHistory.items():
            url = h.originalUrl()
            icon = QWebSettings.iconForUrl(url)
            self.popUp.addItem(QListWidgetItem(icon, h.title()))
            
        self.popUp.setWindowTitle('History')
        self.popUp.setMinimumSize(400, 400)
        
        self.popUp.itemActivated.connect(self.doubleClickHistory)
        self.popUp.itemClicked.connect(self.showHistoryRightClick)
        self.popUp.show()
        
    def doubleClickHistory(self, item):
        for i in range(0, self.searchHistory.count()):
            if(self.searchHistory.itemAt(i).title() == item.text()):
                self.web.load(self.searchHistory.itemAt(i).originalUrl())
                break
    
    def showHistoryRightClick(self, item):
        
        self.popUp.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.historyRightClickMenu = QMenu()
        
        self.item = item
        
        menuItem = self.historyRightClickMenu.addAction('Open')
        menuItem.triggered.connect(self.openHistory)
        
        menuItem = self.historyRightClickMenu.addAction('Open in a New Tab')
        
        menuItem = self.historyRightClickMenu.addAction('Bookmark page')
        
        menuItem = self.historyRightClickMenu.addAction('Delete page')
        
        self.popUp.customContextMenuRequested.connect(self.showHistoryRightClickMenu)
    
    
    def showHistoryRightClickMenu(self, QPos):
        parentPosition = self.popUp.mapToGlobal(QPoint(0, 0))        
        menuPosition = parentPosition + QPos
        self.historyRightClickMenu.move(menuPosition)
        self.historyRightClickMenu.show() 
        
    
    def openHistory(self):
        for i in range(0, self.searchHistory.count()):
            if(self.searchHistory.itemAt(i).title() == self.item.text()):
                self.web.load(self.searchHistory.itemAt(i).originalUrl())
                break
#############################################

# Bookmark Button
        
    def bookmarksButtonPush(self):
        self.popUp = QListWidget()
        
        file = open('bookmarks.txt', 'r')
        
        for line in file:
            list = line.split(';')
            url = QUrl(list[1])
            icon = QWebSettings.iconForUrl(url)
            self.popUp.addItem(QListWidgetItem(icon, list[0].strip()))
        
        
        self.popUp.setWindowTitle('Bookmarks')
        self.popUp.setMinimumSize(400, 400)
        
        self.popUp.itemClicked.connect(self.showBookmarkRightClick)
        
        self.popUp.itemActivated.connect(self.doubleClickBookmark)
        
        self.popUp.show()
        
        file.close()
        
        
        
    def doubleClickBookmark(self, item):
        file = open('bookmarks.txt', 'r')
        
        for line in file:
            list = line.split(';')
            if(list[0].strip() == item.text().strip()):
                q = QUrl(list[1].strip())
                if(q.scheme() == ""):
                    q.setScheme("http")
                self.web.load(q)
    
        file.close()
        
    def showBookmarkRightClick(self, item):
        
        self.popUp.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.bookmarkRightClickMenu = QMenu()
        
        self.item = item
        menuItem = self.bookmarkRightClickMenu.addAction('Open')
        menuItem.triggered.connect(self.openBookmark)
        
        menuItem = self.bookmarkRightClickMenu.addAction('Open in a New Tab')
        
        menuItem = self.bookmarkRightClickMenu.addAction('Delete bookmark')
        menuItem.triggered.connect(self.deleteBookmark)
        
        self.popUp.customContextMenuRequested.connect(self.showBookmarkRightClickMenu)
    
    
    def showBookmarkRightClickMenu(self, QPos):
        parentPosition = self.popUp.mapToGlobal(QPoint(0, 0))        
        menuPosition = parentPosition + QPos
        self.bookmarkRightClickMenu.move(menuPosition)
        self.bookmarkRightClickMenu.show() 
        
    def openBookmark(self):
        file = open('bookmarks.txt', 'r')
        
        for line in file:
            list = line.split(';')
            if(list[0].strip() == self.item.text().strip()):
                q = QUrl(list[1].strip())
                if(q.scheme() == ""):
                    q.setScheme("http")
                self.web.load(q)
    
        file.close()
        
    def deleteBookmark(self):
        file = open('bookmarks.txt', 'r')
        
        lines = file.readlines()
        file.close()
        file = open('bookmarks.txt', 'w')
        for line in lines:
            list = line.split(';')
            if(list[0].strip() != self.item.text().strip()):
                file.write(line)
        self.item.setHidden(True)
    
        file.close()
#################################################

# AddBookmark Button
    
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
###########################################
        

    def forwardButtonPush(self):
        self.searchHistory.forward()
        
    def backButtonPush(self):
        self.searchHistory.back()

    def refreshButtonPush(self):
        self.web.reload()

    def homeButtonPush(self):
        self.web.load(self.homePage)

    def goButtonPush(self, address):
        tmp = address
        
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
        
  

def main():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.showMaximized()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 
