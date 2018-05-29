import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import * 

class Youtube(QMainWindow):
    
    def __init__(self, page, parent=None):
        super(Youtube, self).__init__(parent)
        
        self.setFixedSize(1200, 800)
        
        web = QWebView()
        web.load(QUrl('http://' + page.lower()))
        
        view = QGraphicsView(self)
        view.setFixedSize(1200, 800)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        _layout = QVBoxLayout(view)
        
        scene = QGraphicsScene(self)
        
        _layout.addWidget(web)
        view.setScene(scene)
        
  
