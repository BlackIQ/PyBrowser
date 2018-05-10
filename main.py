import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import * 

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle('Browser')
        self.setWindowIcon(QIcon('web.png'))
        
        self.main_bar = MainBar(self) 
        self.web = QWebView()
        self.web.load(QUrl('https://www.google.com'))

        _widget = QWidget() 
        _layout = QVBoxLayout(_widget)
        #add widgets here
        _layout.addWidget(self.main_bar)
        _layout.addWidget(self.web)
        _layout.setAlignment(Qt.AlignTop)

        self.setCentralWidget(_widget)
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm close',
        "You are about to exit. Are you sure you want to continue?", QMessageBox.Yes | 
        QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

class MainBar(QWidget):

    def __init__(self, parent):
        super(MainBar, self).__init__(parent)
        self.__controls()
        self.__layout()


    def goButtonPush(self):
        #TODO 
        asd = 5
    def __controls(self):
        self.back = QPushButton('back')
        self.forward = QPushButton('forward')
        self.refresh = QPushButton('refresh')
        self.home = QPushButton('home')
        self.settings = QPushButton('settings')
        self.history = QPushButton('history')
        self.bookmarks = QPushButton('bookmarks')
        self.addressBar = QLineEdit()
        self.go = QPushButton('go')
        
        self.go.clicked.connect(self.goButtonPush)

    def __layout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.back)
        hbox.addWidget(self.forward)
        hbox.addWidget(self.refresh)
        hbox.addWidget(self.home)
        hbox.addWidget(self.addressBar)   
        hbox.addWidget(self.go)
        hbox.addWidget(self.bookmarks)
        hbox.addWidget(self.history)
        hbox.addWidget(self.settings)                
        self.setLayout(hbox)


def main():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 
