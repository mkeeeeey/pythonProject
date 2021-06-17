import socket
import struct

from PyQt5.QtWidgets import QMessageBox

from Event.Setting import var_dic
from Util.Log import Logger

# 소켓생성
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

global check
check = False


def connServer(self):
    global HOST, PORT
    HOST = var_dic['tcp']['ip']
    PORT = var_dic['tcp']['port']
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(3)
    global check
    if check:
        client_socket.close()
        check = False
    try:
        client_socket.connect((HOST,PORT))
        print('Client connect server')
        check = True
        QMessageBox.information(self, 'Message', '연결되었습니다\n')
        self.singleFrame.setEnabled(True)
        self.LoopFrame.setEnabled(True)
    except OSError as ose:
        print(ose)
        QMessageBox.information(self, 'Error', '연결할 수 없습니다.\n'+str(ose))
        self.singleFrame.setEnabled(False)
        self.LoopFrame.setEnabled(False)
    except Exception as e:
        print(e)
        QMessageBox.information(self, 'Error', '연결할 수 없습니다.\n' + str(e))
        self.singleFrame.setEnabled(False)
        self.LoopFrame.setEnabled(False)



def send_msg(self, msg):
    if msg[2:4] == '10':
        data = struct.pack('>BBHHBBHHB',
                           16, 0, 0, len(msg) // 2, int(msg[0:2], 16), int(msg[2:4], 16),
                           # Transaction ID / Protocol ID / Length / Unit ID / Function Code
                           int(msg[4:8], 16), int(msg[8:12], 16),
                           int(msg[12:14], 16))  # D-Register / Num. of Data / byte of Data /
        for i in range(len(msg)-14):
            x = i + 14
            if x % 4 == 2:
                data = data + struct.pack('>H', int(msg[x:x+4], 16)) # Data
    else:
        data = struct.pack('>BBHHBBHH',
                           16, 0, 0, 6, int(msg[0:2], 16), int(msg[2:4], 16), # Transaction ID / Protocol ID / Length / Unit ID / Function Code
                           int(msg[4:8], 16), int(msg[8:12], 16))  # D-Register / Data

    client_socket.send(data)
    print(data.hex())
    self.TxText.append(data.hex().upper())
    req = client_socket.recv(1024)
    print(req.hex())
    self.RxText.append(req.hex().upper())
    if self.saveBtn.isChecked():
        Logger.info('Tx : ' + data.hex().upper())
        Logger.info('Rx : ' + req.hex().upper())


def stopSock():
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
        print('stop!')
        client_socket.connect((HOST, PORT))
    except socket.error as err:
        print(err)
        pass


def closeSock():
    global check
    check = False
#     global client_socket
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         # client_socket.shutdown(socket.SHUT_RDWR)
#         client_socket.close()
#     except socket.error as err:
#         print(err)
#         pass