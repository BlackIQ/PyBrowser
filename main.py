import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon

class prva(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.resize(700, 700)
        self.center()
        self.setWindowTitle('Browser')
        self.setWindowIcon(QIcon('web.png'))
        
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
