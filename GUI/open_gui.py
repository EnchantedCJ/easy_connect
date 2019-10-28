# -*- coding: utf-8 -*-
import sys
import os
import json
import subprocess

from GUI import main_window
from PyQt5 import QtCore, QtGui, QtWidgets


# from PyQt5.QtWidgets import QMessageBox, QFileDialog, QProgressDialog
# from PyQt5.QtCore import Qt


class MyMainDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = main_window.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.lineEdit_ip.setDisabled(True)

        self._buildSignalAndSlot()
        self._ipt_config()
        self._init_comboBox()

    # signals and slots
    def _buildSignalAndSlot(self):
        self.ui.comboBox_name.currentTextChanged.connect(self._get_info)
        self.ui.pushButton_connect.clicked.connect(self._connect)

    def _ipt_config(self):
        with open('config.json', 'r', encoding='utf-8') as f:
            configText = f.read()
        self.config = json.loads(configText)

    def _init_comboBox(self):
        for key in self.config['servers']:
            self.ui.comboBox_name.addItems([key])

    def _get_info(self):
        name = self.ui.comboBox_name.currentText()
        server = self.config['servers'][name]
        if server['port'] != '':
            ip_port = server['IP'] + ':' + server['port']
        else:
            ip_port = server['IP']
        users = server['Users']

        self.ui.lineEdit_ip.setText(ip_port)
        self.ui.comboBox_user.clear()
        for key in users:
            self.ui.comboBox_user.addItems([key])

    def _connect(self):
        name = self.ui.comboBox_name.currentText()
        server = self.config['servers'][name]
        ip = server['IP']
        if server['port'] != '':
            ip_port = server['IP'] + ':' + server['port']
        else:
            ip_port = server['IP']
        username = self.ui.comboBox_user.currentText()
        password = server['Users'][username]['pass']

        subprocess.run('cmdkey /generic:TERMSRV/{ip} /user:{username} /pass:{password}'.format(ip=ip,
                                                                                               username=username,
                                                                                               password=password),
                       shell=False)
        subprocess.run('mstsc /v:{ip}'.format(ip=ip_port), shell=False)
        subprocess.run('cmdkey /delete:TERMSRV/{ip}'.format(ip=ip), shell=False)


#

def exec():
    app = QtWidgets.QApplication(sys.argv)
    MainDialog = MyMainDialog()
    MainDialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    exec()
