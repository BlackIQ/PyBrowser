import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import * 

class Window(QGraphicsScene):
    
    def __init__(self, view):
        super(Window, self).__init__(view)
        
        _layout = QVBoxLayout(view)

        self.view = view
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.currentChanged.connect(self.currentTabChanged)
        self.tabs.tabCloseRequested.connect(self.closeCurrentTab)
        
        self.history = [] # list of strings, string = "title;URL" needed for writing history in a file
        self.historyForEachTab = {} # key = tabIndex, value = tabIndexHistory - needed for back and forward methods
        self.addNewTab()
    
        button = QPushButton(QIcon('plus.png'), '')
        button.setStatusTip('Open a new tab')
        button.clicked.connect(self.addNewTab) 
        self.tabs.setCornerWidget(button, Qt.TopLeftCorner)

        self.setBackgroundBrush(QBrush(QColor(230, 230, 230)))
        
        _layout.addWidget(self.tabs)

    def addNewTab(self):

        qurl = QUrl('www.google.com')

        web = QWebView()
        web.load(QUrl("https://www.google.com"))

        i = self.tabs.addTab(web, "Google")

        self.tabs.setCurrentIndex(i)
        
        web.urlChanged.connect(lambda qurl, web=web: self.update_urlbar(qurl, web))
        web.loadFinished.connect(lambda _, i=i, web=web: self.tabs.setTabText(i, web.title()))
        web.loadFinished.connect(lambda _, qurl=qurl, web=web: self.addToHistory(web.title(), web.url().toString()))
        
        self.historyForEachTab[i] = self.tabs.currentWidget().page().history()
        
    def addToHistory(self, title, link):
           
        if(len(self.history) == 0):
            self.history.append(''.join((title, ';', link)))
            return
           
        if(self.history[-1] != ''.join((title, ';', link))):
            self.history.append(''.join((title, ';', link)))

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        self.parent().parent().addressBar.setText(q.toString()) 

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
        self.popUp = QWidget()
            
        self.popUp.setWindowTitle('History')
        self.popUp.setMinimumSize(400, 400)
        
        layout = QVBoxLayout()
        
        self.list = QListWidget()
        
        file = open('history.txt', 'r')
        
        for line in file:
            list = line.split(';')
            url = QUrl(list[1])
            self.list.addItem(QListWidgetItem(list[0].strip() + '  -  ' + list[1].strip()))
            
        file.close()
        
        for line in self.history:
            list = line.split(';')
            url = QUrl(list[1])
            self.list.addItem(QListWidgetItem(list[0].strip() + '  -  ' + list[1].strip()))
        
        button = QPushButton('Delete History')
        button.clicked.connect(self.deleteAllHistory)
        
        layout = QVBoxLayout()
        layout.addWidget(self.list)
        layout.addWidget(button)
        self.popUp.setLayout(layout)
        
        self.list.itemActivated.connect(self.doubleClickHistory)
        self.list.itemClicked.connect(self.leftClickOnHistoryListElement)
        
        self.popUp.show()
        
    def doubleClickHistory(self, item):
        list = item.text().split('  -  ')
        self.tabs.currentWidget().load(QUrl(list[1]))
        
        self.popUp.close()
    
    def leftClickOnHistoryListElement(self, item):
        
        self.popUp.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.historyRightClickMenu = QMenu()
        
        self.item = item
        
        menuItem = self.historyRightClickMenu.addAction('Open')
        menuItem.triggered.connect(self.openHistory)
        
        menuItem = self.historyRightClickMenu.addAction('Open in a New Tab')
        menuItem.triggered.connect(self.openHistoryInNewTab)
        
        menuItem = self.historyRightClickMenu.addAction('Bookmark page')
        menuItem.triggered.connect(self.addBookmarkFromHistory)
        
        
        self.popUp.customContextMenuRequested.connect(self.showHistoryRightClickMenu)
    
    def deleteAllHistory(self):
        self.history = []
        file = open('history.txt', 'r')
        
        lines = file.readlines()
        file.close()
        
        file = open('history.txt', 'w')
        for line in lines:
            file.write('')
        file.close()
        
        self.popUp.close()
    
    def showHistoryRightClickMenu(self, QPos):
        parentPosition = self.popUp.mapToGlobal(QPoint(0, 0))        
        menuPosition = parentPosition + QPos
        self.historyRightClickMenu.move(menuPosition)
        self.historyRightClickMenu.show() 
        
    
    def openHistory(self):
        list = self.item.text().split('  -  ')
        self.tabs.currentWidget().load(QUrl(list[1]))
        
        print(list[1])
            
        self.popUp.close()
        
    def openHistoryInNewTab(self):
        list = self.item.text().split('  -  ')
        q = QUrl(list[1])
        
        web = QWebView()
        web.load(q)
        web.setMinimumHeight(qApp.primaryScreen().size().height()-160)

        i = self.tabs.addTab(web, "Google")

        self.tabs.setCurrentIndex(i)

        web.urlChanged.connect(lambda qurl, web=web: self.update_urlbar(qurl, web))
        web.loadFinished.connect(lambda _, i=i, web=web: self.tabs.setTabText(i, web.title()))
        web.loadFinished.connect(lambda _, qurl=qurl, web=web: self.addToHistory(web.title(), web.url().toString()))
        self.popUp.close()
        
        
    def addBookmarkFromHistory(self):
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
        
#############################################

# Bookmark Button
        
    def bookmarksButtonPush(self):
        self.popUp = QWidget()
        
        self.popUp.setWindowTitle('Bookmarks')
        self.popUp.setMinimumSize(400, 400)
        
        self.list = QListWidget()
        
        file = open('bookmarks.txt', 'r')
        
        for line in file:
            list = line.split(';')
            url = QUrl(list[1])
            self.list.addItem(QListWidgetItem(list[0].strip()))
        
        file.close()
        
        layout = QVBoxLayout()
        layout.addWidget(self.list)
        
        self.popUp.setLayout(layout)
        
        self.list.itemClicked.connect(self.leftClickOnBookmarkListElement)
        
        self.list.itemActivated.connect(self.doubleClickBookmark)
        
        self.popUp.show()
        
        
        
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
        self.popUp.close()
        
    def leftClickOnBookmarkListElement(self, item):
        
        self.popUp.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.bookmarkRightClickMenu = QMenu()
        
        self.item = item
        menuItem = self.bookmarkRightClickMenu.addAction('Open')
        menuItem.triggered.connect(self.openBookmark)
        
        menuItem = self.bookmarkRightClickMenu.addAction('Open in a New Tab')
        menuItem.triggered.connect(self.openBookmarkInNewTab)
        
        menuItem = self.bookmarkRightClickMenu.addAction('Delete bookmark')
        menuItem.triggered.connect(self.deleteBookmark)
        
        self.popUp.customContextMenuRequested.connect(self.showBookmarkRightClickMenu)
    
    
    def showBookmarkRightClickMenu(self, QPos):
        parentPosition = self.popUp.mapToGlobal(QPoint(0, 0))        
        menuPosition = parentPosition + QPos
        self.bookmarkRightClickMenu.move(menuPosition)
        self.bookmarkRightClickMenu.show() 
        
    def openBookmarkInNewTab(self):
        
        file = open('bookmarks.txt', 'r')
        
        global q
        
        for line in file:
            list = line.split(';')
            if(list[0].strip() == self.item.text().strip()):
                q = QUrl(list[1].strip())
                if(q.scheme() == ""):
                    q.setScheme("http")
    
        file.close()
        
        web = QWebView()
        web.load(q)
        web.setMinimumHeight(qApp.primaryScreen().size().height()-160)

        i = self.tabs.addTab(web, "Google")

        self.tabs.setCurrentIndex(i)

        web.urlChanged.connect(lambda qurl, web=web: self.update_urlbar(qurl, web))
        web.loadFinished.connect(lambda _, i=i, web=web: self.tabs.setTabText(i, web.title()))
        
        self.popUp.close()
        
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
        
        self.popUp.close()
        
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
        
        button.clicked.connect(self.saveBookmark)
        
        self.popUp.setWindowTitle('Page Bookmarked')
        self.popUp.setMaximumSize(300, 200)
        
        self.popUp.show()

    def saveBookmark(self):
        file = open('bookmarks.txt', 'a+')
        
        for line in file:
            list = line.split(';')
            if(list[0] == self.add.text()):
                return
        
        if(self.add.text().strip() != ''):
            file.write(self.add.text() + ';' + self.tabs.currentWidget().url().toString() + '\n')
            self.popUp.close()
            
        file.close()
###########################################
        

    def forwardButtonPush(self):
        self.historyForEachTab[self.tabs.currentIndex()].forward()
        
    def backButtonPush(self):
        self.historyForEachTab[self.tabs.currentIndex()].back()

    def refreshButtonPush(self):
        self.tabs.currentWidget().reload()

    def homeButtonPush(self):
        self.tabs.currentWidget().load(QUrl('https://www.google.com/'))

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
        
  
