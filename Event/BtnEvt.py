# 단일실행
def singleEvt(self):
    self.LoopFrame.hide()
    self.singleFrame.show()


# 반복실행
def loopEvt(self):
    self.singleFrame.hide()
    self.LoopFrame.show()


# Function Code
def autoCode(self, code):
    addr = format(self.addrSpin.value(), 'X').zfill(2)
    if self.singleBtn.isChecked():
        self.lineTxt.setText(addr + code)
    elif self.loopBtn.isChecked():
        self.loopTxt.appendPlainText(addr + code)


# Communication Type
def tabType(self):
    if self.tcpBtn.isChecked():
        self.TypeTab.setCurrentIndex(1)
        self.serBtn.setEnabled(False)
        self.etherBtn.setEnabled(True)
    else:
        self.TypeTab.setCurrentIndex(0)
        self.serBtn.setEnabled(True)
        self.etherBtn.setEnabled(False)


def moveTab(self):
    cur_index = self.TypeTab.currentIndex()
    if cur_index == 1:
        self.tcpBtn.setChecked(True)
        self.serBtn.setEnabled(False)
        self.etherBtn.setEnabled(True)
    elif cur_index == 0:
        self.rtuBtn.setChecked(True)
        self.serBtn.setEnabled(True)
        self.etherBtn.setEnabled(False)


# Text Browser Clear
def winClear(self):
    self.loopTxt.clear()
    self.TxText.clear()
    self.RxText.clear()
