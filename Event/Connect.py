from Event.Setting import var_dic, save_dic
from Util.SerialComm import ser_open, ser_close
from Util.TCPclient import connServer, closeSock


def Conn(self):
    closeSock()
    ser_close()
    if self.tcpBtn.isChecked():
        var_dic['type'] = 'tcp'
        var_dic['tcp']['ip'] = self.ipTxt.text()
        var_dic['tcp']['port'] = int(self.portTxt.text())
        var_dic['delay time'] = int(self.dtTxt2.text())
        connServer(self)
    else:
        if self.rtuBtn.isChecked():
            var_dic['type'] = 'rtu'
        elif self.rtuBtn.isChecked():
            var_dic['type'] = 'ascii'
        var_dic['ser']['com port'] = self.port_box.currentText()
        var_dic['ser']['baud rate'] = int(self.speed_box.currentText())
        var_dic['ser']['parity'] = self.parity_box.currentText()
        var_dic['ser']['stop bits'] = int(self.stopbit_box.currentText())
        var_dic['ser']['data bits'] = int(self.databit_box.currentText())
        var_dic['delay time'] = int(self.dtTxt1.text())
        ser_open(self)
    save_dic(str(var_dic))
