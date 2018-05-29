from mainWindow import *
from youtube import *


def main():
    app = QApplication(sys.argv)

    if len(sys.argv) < 2:
        win = MainWindow()
        win.showMaximized()
    else:
        win = Youtube(sys.argv[1])
        win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 
