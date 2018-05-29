from window import *

class Browser(QGraphicsView):

    def __init__(self, parent):
        super(Browser, self).__init__(parent)
        self.page = Window(self)
        
        self.setScene(self.page)
        
