import sys
import threading
from time import sleep

from PyQt5.QtCore import QObject, QEventLoop, pyqtSignal
from PyQt5.QtWidgets import QApplication

from Event.Setting import var_dic
from Util import LRC, CRC16
from Util.Log import setLog, Logger
from Util.SerialComm import read_serial, read_rtu
from Util.TCPclient import send_msg, stopSock


# Single Input
def singleIn(self):
    if self.saveBtn.isChecked():
        setLog()
    txt = self.lineTxt.text()
    if var_dic['type'] == 'ascii':
        singleLRC(self, txt)
    elif var_dic['type'] == 'rtu':
        singleCRC(self, txt)
    elif var_dic['type'] == 'tcp':
        send_msg(self, txt)
    self.lineTxt.clear()


def singleLRC(self, txt):
    lrc = LRC.calLRC(self, txt)
    print('데이터 전송 확인')
    sleep(var_dic['delay time'] / 1000)
    print('딜레이')
    self.TxText.append(lrc)
    print('쓰기' + lrc)
    rxd = read_serial() + '[CR][LF]'
    self.RxText.append(rxd)
    if self.saveBtn.isChecked():
        Logger.info('Rx : ' + rxd)


def singleCRC(self, txt):
    CRC16.calCRC(self, txt)
    sleep(var_dic['delay time'] / 1000)
    if txt[3] == '3':
        cnt = int(txt[8:13], 16) * 2
        rxd = read_rtu(3 + cnt + 2)
    else:
        rxd = read_rtu(8)
    self.RxText.append(rxd)
    if self.saveBtn.isChecked():
        Logger.info('Rx : ' + rxd)


# For Loop
switch = False


# Loop Input
def loopIn(self):
    lines = self.loopTxt.toPlainText().strip()
    global switch
    switch = True
    self.loop_inBtn.setEnabled(False)
    self.stopBtn.setEnabled(True)
    if var_dic['type'] == 'ascii':
        th = threading.Thread(target=loopLRC, args=(self, lines))
        th.start()
    elif var_dic['type'] == 'rtu':
        th = threading.Thread(target=loopCRC, args=(self, lines))
        th.start()
    elif var_dic['type'] == 'tcp':
        th = threading.Thread(target=loopTCP, args=(self, lines))
        th.start()


def loopLRC(self, lines):
    while switch:
        for line in lines.split('\n'):
            if switch:
                lrc = LRC.calLRC(self, line)
                sleep(var_dic['delay time'] / 1000)
                self.TxText.append(lrc)
                rxd = read_serial() + '[CR][LF]'
                self.RxText.append(rxd)
                if self.saveBtn.isChecked():
                    Logger.info('Rx : '+rxd)
                sleep(var_dic['delay time'] / 1000)
                QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
            else:
                break


def loopCRC(self, lines):
    while switch:
        for line in lines.split('\n'):
            if switch:
                CRC16.calCRC(self, line)
                sleep(var_dic['delay time'] / 1000)
                if line[3] == '3':
                    cnt = int(line[8:13], 16) * 2
                    rxd = read_rtu(3 + cnt + 2)
                else:
                    rxd = read_rtu(8)
                self.RxText.append(rxd)
                if self.saveBtn.isChecked():
                    Logger.info('Rx : '+rxd)
                sleep(var_dic['delay time'] / 1000)
                # textbrowser에 한 줄 씩 나타내기 위한 이벤트
                QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
            else:
                break


def loopTCP(self, lines):
    while switch:
        for line in lines.split('\n'):
            if switch:
                send_msg(self, line)
                sleep(var_dic['delay time'] / 1000)
                QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
            else:
                stopSock()
                break


def stop(self):
    global switch
    switch = False
    self.loop_inBtn.setEnabled(True)
    self.stopBtn.setEnabled(False)


# textbrowser에 한 줄씩 나타내기 위한 Class
class StdoutRedirect(QObject):
    printOccur = pyqtSignal(str, str, name="print")

    def __init__(self, *param):
        QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg: self.write(msg, color="red")

    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)