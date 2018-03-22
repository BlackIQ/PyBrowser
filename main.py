import sys
from mainBar import MainBar
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle('Browser')
        self.setWindowIcon(QIcon('web.png'))
        
        self.main_bar = MainBar(self) 
        _widget = QWidget() 
        _layout = QVBoxLayout(_widget)
        #add widgets here
        _layout.addWidget(self.main_bar)
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

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 
