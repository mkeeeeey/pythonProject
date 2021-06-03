from PyQt5 import uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *

from Event import BtnEvt, Connect, InputEvt
from Event.Setting import setting
from Util import translate

form_class = uic.loadUiType('Window/Mainwindow.ui')[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        setting(self)

        regExp = QRegExp("[A-Za-z0-9]*")
        self.lineTxt.setValidator(QRegExpValidator(regExp))

        # Send data Box
        self.singleBtn.clicked.connect(lambda : BtnEvt.singleEvt(self))
        self.loopBtn.clicked.connect(lambda : BtnEvt.loopEvt(self))
        # Function code
        self.fc03.clicked.connect(lambda : BtnEvt.autoCode(self, '03'))
        self.fc06.clicked.connect(lambda : BtnEvt.autoCode(self, '06'))
        self.fc16.clicked.connect(lambda : BtnEvt.autoCode(self, '10'))
        # Comm. Type
        self.rtuBtn.clicked.connect(lambda : BtnEvt.tabType(self))
        self.asciiBtn.clicked.connect(lambda : BtnEvt.tabType(self))
        self.tcpBtn.clicked.connect(lambda : BtnEvt.tabType(self))
        # Tab
        self.TypeTab.currentChanged.connect(lambda : BtnEvt.moveTab(self))
        # Connect
        self.serBtn.clicked.connect(lambda : Connect.Conn(self))
        self.etherBtn.clicked.connect(lambda : Connect.Conn(self))
        # Input
        self.single_inBtn.clicked.connect(lambda : InputEvt.singleIn(self))
        self.loop_inBtn.clicked.connect(lambda : InputEvt.loopIn(self))
        self.stopBtn.clicked.connect(lambda : InputEvt.stop(self))
        # Clear
        self.TxClearBtn.clicked.connect(lambda : BtnEvt.winClear(self))
        # Language
        self.korBtn.clicked.connect(lambda : translate.Kor(self))
        self.engBtn.clicked.connect(lambda : translate.Eng(self))