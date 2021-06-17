import serial
from PyQt5.QtWidgets import QMessageBox

from Event.Setting import var_dic

com_port = var_dic['ser']['com port']
baud_rate = var_dic['ser']['baud rate']
if var_dic['ser']['parity'] == 'NONE':
    parity = serial.PARITY_NONE
elif var_dic['ser']['parity'] == 'ODD':
    parity = serial.PARITY_ODD
elif var_dic['ser']['parity'] == 'EVEN':
    parity = serial.PARITY_EVEN
if var_dic['ser']['stop bits'] == 1:
    stop_bits = serial.STOPBITS_ONE
elif var_dic['ser']['stop bits'] == 2:
    stop_bits = serial.STOPBITS_TWO
if var_dic['ser']['data bits'] == 7:
    data_bits = serial.SEVENBITS
elif var_dic['ser']['data bits'] == 8:
    data_bits = serial.EIGHTBITS
dt = var_dic['delay time']


def ser_open(self):
    global ser
    ser = serial.Serial()
    ser.port = com_port
    ser.baudrate = baud_rate
    ser.parity = parity
    ser.stopbits = stop_bits
    ser.bytesize = data_bits
    try:
        if ser.isOpen():
            ser.close()
            ser.open()
            self.singleFrame.setEnabled(True)
            self.LoopFrame.setEnabled(True)
        else:
            ser.open()
            self.singleFrame.setEnabled(True)
            self.LoopFrame.setEnabled(True)
        QMessageBox.information(self, 'Message', '연결되었습니다\n')
    except Exception as ex:
        print('COM PORT OPEN ERROR:', ex)
        QMessageBox.warning(self, 'Message', '연결할 수 없습니다\n')
        self.singleFrame.setEnabled(False)
        self.LoopFrame.setEnabled(False)


def send_serial(data):
    if ser.isOpen():
        ser.write(data)


def read_serial():
    if ser.readable():
        res = ser.readline()
        return res.decode()[:len(res) - 2]


def read_rtu(cnt):
    print('동작확인')
    if ser.readable():
        print('readable')
        res = ser.read(size=cnt).hex().upper()
        print('결과:'+res)
        return res


def ser_close():
    global ser
    ser = serial.Serial()
    ser.port = com_port
    ser.baudrate = baud_rate
    ser.parity = parity
    ser.stopbits = stop_bits
    ser.bytesize = data_bits
    if ser.isOpen():
        ser.close()