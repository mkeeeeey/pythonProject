import sys
from PyQt5.QtWidgets import *
from Window.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindow()
    view.show()

    sys.exit(app.exec_())