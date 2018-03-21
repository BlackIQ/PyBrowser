import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
class prva(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.resize(1000, 800)
        self.center()
        self.setWindowTitle('Browser')
        self.setWindowIcon(QIcon('web.png'))
        
        back = QPushButton('back')
        forward = QPushButton('forward')
        refresh = QPushButton('refresh')
        home = QPushButton('home')
        
        settings = QPushButton('settings')
        history = QPushButton('history')
        bookmarks = QPushButton('bookmarks')
        
        addressBar = QLineEdit()
        
        hbox = QHBoxLayout()
        
        hbox.addWidget(back)
        hbox.addWidget(forward)
        hbox.addWidget(refresh)
        hbox.addWidget(home)
        hbox.addWidget(addressBar)   
        hbox.addWidget(bookmarks)
        hbox.addWidget(history)
        hbox.addWidget(settings)        
        
        
        
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.setAlignment(Qt.AlignTop)
        
        self.setLayout(vbox)
        
        self.show()
    
    #Moving program to screen center
    def center(self):
        
        #Get main window rectangle
        qr = self.frameGeometry()
        #Get screen center 
        cp = QDesktopWidget().availableGeometry().center()
        #Move window rectangle center to screen center 
        qr.moveCenter(cp)
        #Move top-left application point to top-left point on centered rectangle 
        self.move(qr.topLeft())
        
    #We must override this method which is called when exiting program
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Confirm close',
            "You are about to exit. Are you sure you want to continue?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    w = prva()
    sys.exit(app.exec_())
