from browser import *

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent) #super(subClass, instance).__init__(parent)
        self.setGeometry(10, 10, 1000, 800) #setGeometry(topLeftX, topLeftY, width, height)
        
        self.setWindowTitle('Browser')
        self.setWindowIcon(QIcon('web.png'))
        

        self.addressBar = QLineEdit()
        self.addressBar.setPlaceholderText('Search with Google or enter address')
        
        self.createBrowser() # Method that creates graphics view 
        
        #---------------------Toolbar buttons section-----------------------
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
        
        self.goAction = QAction(QIcon('search.png'), 'Go', self)
        self.goAction.setShortcut(Qt.Key_Return)
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
        
        
        
        tb.addAction(self.backAction)
        tb.addAction(self.forwardAction)
        tb.addAction(self.refreshAction)
        tb.addAction(self.homeAction)
        tb.addWidget(self.addressBar)
        tb.addAction(self.goAction)
        tb.addAction(self.bookmarkAction)
        tb.addAction(self.historyAction)
        tb.addAction(self.bookmarksAction)

        
        
    def createBrowser(self):
        self.browser = Browser(self)
        self.setCentralWidget(self.browser)
        
        
    def closeEvent(self, event):  
        
        file = open('history.txt', 'a+', encoding='utf-8') # a+ mode opens in read+write, appending to end of file and creating file if it doesn't exist
        
        
        for i in self.browser.page.history:
            file.write((i + '\n'))
            
        file.close()
        
        reply = QMessageBox.question(self, 'Confirm close',
        "You are about to exit. Are you sure you want to continue?", QMessageBox.Yes | 
        QMessageBox.No, QMessageBox.Yes) # parent, title, message, buttons, default button

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
            
