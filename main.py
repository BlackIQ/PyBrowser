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
        self.backAction = QAction(QIcon('back.png'), 'Back', self)
        self.backAction.setShortcut('Ctrl+B')
        self.backAction.triggered.connect(self.browser.page.backButtonPush)

        self.forwardAction = QAction(QIcon('forward.png'), 'Forward', self)
        self.forwardAction.setShortcut('Ctrl+F')
        self.forwardAction.triggered.connect(self.browser.page.forwardButtonPush)

        self.refreshAction = QAction(QIcon('refresh.png'), 'Refresh', self)
        self.refreshAction.setShortcut('Ctrl+R')
        self.refreshAction.triggered.connect(self.browser.page.refreshButtonPush)

        self.homeAction = QAction(QIcon('home.png'), 'Home', self)
        self.homeAction.setShortcut('Ctrl+H')
        self.homeAction.triggered.connect(self.browser.page.homeButtonPush)
        
        self.addressBar = QLineEdit()
        self.addressBar.setPlaceholderText('Search with Google or enter address')
        self.addressBar.editingFinished.connect(lambda: self.browser.page.goButtonPush(self.addressBar.text()))
        
        self.goAction = QAction(QIcon('search.png'), 'Go', self)
        self.goAction.setShortcut('Ctrl+S')
        self.goAction.triggered.connect(lambda: self.browser.page.goButtonPush(self.addressBar.text()))
        
                    
        self.bookmarkAction = QAction(QIcon('star.png'), 'Add bookmark', self)
        self.bookmarkAction.setShortcut('Ctrl+B')
        self.bookmarkAction.triggered.connect(self.browser.page.addBookmarkPush)
            
        self.historyAction = QAction(QIcon('history.png'), 'History', self)
        self.historyAction.setShortcut('Ctrl+H')
        self.historyAction.triggered.connect(self.browser.page.historyButtonPush)
            
        self.bookmarksAction = QAction(QIcon('bookmarks.png'), 'Bookmarks', self)
        self.bookmarksAction.setShortcut('Ctrl+V')
        self.bookmarksAction.triggered.connect(self.browser.page.bookmarksButtonPush)
            
        self.settingsAction = QAction(QIcon('settings.png'), 'Settings', self)
        self.settingsAction.setShortcut('Ctrl+O')
        self.settingsAction.triggered.connect(self.browser.page.refreshButtonPush)
        
        
        
        tb.addAction(self.backAction)
        tb.addAction(self.forwardAction)
        tb.addAction(self.refreshAction)
        tb.addAction(self.homeAction)
        tb.addWidget(self.addressBar)
        tb.addAction(self.goAction)
        tb.addAction(self.bookmarkAction)
        tb.addAction(self.historyAction)
        tb.addAction(self.bookmarksAction)
        tb.addAction(self.settingsAction)


        fileMenu = self.menuBar().addMenu("&File")

        self.newTabAction =  QAction(QIcon('star.png'), "New tab", self)
        self.newTabAction.setStatusTip("Open a new tab")
        self.newTabAction.triggered.connect(lambda _: self.browser.page.addNewTab()) 
        
        fileMenu.addAction(self.newTabAction)
        
        
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

        self.view = view
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        self.tabs.setTabsClosable(True)
        self.tabs.currentChanged.connect(self.currentTabChanged)
        self.tabs.tabCloseRequested.connect(self.closeCurrentTab)
      
        self.addNewTab()

        self.setBackgroundBrush(QBrush(QColor(230, 230, 230), Qt.SolidPattern))
        
        self.searchHistory = self.tabs.currentWidget().page().history()

        _layout.addWidget(self.tabs)

    def addNewTab(self):

        qurl = QUrl('www.google.com')

        web = QWebView()
        web.load(QUrl("https://www.google.com"))
        web.setMinimumHeight(qApp.primaryScreen().size().height()-160)

        i = self.tabs.addTab(web, "Google")

        self.tabs.setCurrentIndex(i)

        web.urlChanged.connect(lambda qurl, web=web: self.update_urlbar(qurl, web))
        web.loadFinished.connect(lambda _, i=i, web=web: self.tabs.setTabText(i, web.title()))

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        #addressBar.setText(q.toString()) TODO Dohvatiti addressBar iz toolbara. Ne znam kako da dohvatim

    def currentTabChanged(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.updateTitle(self.tabs.currentWidget())

    def updateTitle(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().title()
        self.view.parent().setWindowTitle(title)

    def closeCurrentTab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i) 
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
                self.tabs.currentWidget().load(self.searchHistory.itemAt(i).originalUrl())
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
                self.tabs.currentWidget().load(self.searchHistory.itemAt(i).originalUrl())
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
                self.tabs.currentWidget().load(q)
    
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
                self.tabs.currentWidget().load(q)
    
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
            file.write(self.add.text() + ';' + self.tabs.currentWidget.url().toString() + '\n')
            self.popUp.close()
            
        file.close()
###########################################
        

    def forwardButtonPush(self):
        self.searchHistory.forward()
        
    def backButtonPush(self):
        self.searchHistory.back()

    def refreshButtonPush(self):
        self.tabs.currentWidget().reload()

    def homeButtonPush(self):
        self.tabs.currentWidget().load(self.homePage)

    def goButtonPush(self, address):
        tmp = address
        
        if(tmp == ''):
            return
        
        q = QUrl(tmp)
        if(q.scheme() == ""):
            q.setScheme("http")
            
        if(tmp.find('.') != -1 and tmp.find(' ') == -1):
            self.tabs.currentWidget().load(q)
                
        else:
            l = tmp.split()
            link = 'https://www.google.com/search?q=' + l[0]
            for i in range(1, len(l)):
                link += '+' + l[i]
            self.tabs.currentWidget().load(QUrl(link))
        
  

def main():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.showMaximized()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 
