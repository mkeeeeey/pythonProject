import ast
import copy
from datetime import *

from Util.translate import Kor


# File
def save_dic(data):
    with open('./etc/dictionary.txt', 'w') as file:
        now = datetime.now()
        file.write(now.strftime('%Y-%m-%d %A %H:%M:%S\n'))
        file.write(data)


def get_dic():
    with open('./etc/dictionary.txt', 'r') as file:
        lines = file.readlines()
        read_dic = ast.literal_eval(lines[1])
    return read_dic


# Dictionary
if get_dic() is not None:
    var_dic = copy.deepcopy(get_dic())
else:
    var_dic = {
        'type': 'rtu',
        'ser': {
            'com port': 'COM1',
            'baud rate': 9600,
            'parity': 'NONE',
            'stop bits': 1,
            'data bits': 8
        },
        'tcp': {
            'ip': None,
            'port': None
        },
        'delay time': 500
    }


# Init. Send data
def setting(self):
    self.LoopFrame.hide()
    self.singleFrame.setEnabled(False)
    self.LoopFrame.setEnabled(False)
    if var_dic['type'] == 'tcp':
        self.tcpBtn.setChecked(True)
        self.serBtn.setEnabled(False)
        self.TypeTab.setCurrentIndex(1)
    if var_dic['tcp']['ip'] is not None:
        self.ipTxt.setText(var_dic['tcp']['ip'])
    if var_dic['tcp']['port'] is not None:
        self.portTxt.setText(str(var_dic['tcp']['port']))
    else:
        self.TypeTab.setCurrentIndex(0)
        self.etherBtn.setEnabled(False)
        if var_dic['type'] == 'rtu':
            self.rtuBtn.setChecked(True)
        elif var_dic['type'] == 'ascii':
            self.asciiBtn.setChecked(True)
    self.port_box.setCurrentText(var_dic['ser']['com port'])
    self.speed_box.setCurrentText(str(var_dic['ser']['baud rate']))
    self.parity_box.setCurrentText(var_dic['ser']['parity'])
    self.stopbit_box.setCurrentText(str(var_dic['ser']['stop bits']))
    self.databit_box.setCurrentText(str(var_dic['ser']['data bits']))
    self.dtTxt1.setText(str(var_dic['delay time']))
    self.dtTxt2.setText(str(var_dic['delay time']))
    Kor(self)


