from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

class MainBar(QWidget):

    def __init__(self, parent):
        super(MainBar, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        self. back = QPushButton('back')
        self.forward = QPushButton('forward')
        self.refresh = QPushButton('refresh')
        self.home = QPushButton('home')
        self.settings = QPushButton('settings')
        self.history = QPushButton('history')
        self.bookmarks = QPushButton('bookmarks')
        self.addressBar = QLineEdit()

    def __layout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.back)
        hbox.addWidget(self.forward)
        hbox.addWidget(self.refresh)
        hbox.addWidget(self.home)
        hbox.addWidget(self.addressBar)   
        hbox.addWidget(self.bookmarks)
        hbox.addWidget(self.history)
        hbox.addWidget(self.settings)                
        self.setLayout(hbox)
