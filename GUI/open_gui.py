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
        self.ui.lineEdit_admin.setDisabled(True)

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
        self.name = self.ui.comboBox_name.currentText()
        self.server = self.config['servers'][self.name]
        self.ip = self.server['IP']
        if self.server['port'] != '':
            self.ip_port = self.server['IP'] + ':' + self.server['port']
        else:
            self.ip_port = self.server['IP']
        self.admin=self.server['admin']

        self.ui.lineEdit_ip.setText(self.ip_port)
        self.ui.lineEdit_admin.setText(self.admin)
        self.ui.comboBox_user.clear()
        for key in self.server['Users']:
            self.ui.comboBox_user.addItems([key])

    def _connect(self):
        self.username = self.ui.comboBox_user.currentText()
        self.password = self.server['Users'][self.username]['pass']

        subprocess.run('cmdkey /generic:TERMSRV/{ip} /user:{username} /pass:{password}'.format(ip=self.ip,
                                                                                               username=self.username,
                                                                                               password=self.password),
                       shell=False)
        subprocess.run('mstsc /v:{ip}'.format(ip=self.ip_port), shell=False)
        subprocess.run('cmdkey /delete:TERMSRV/{ip}'.format(ip=self.ip), shell=False)


#

def exec():
    app = QtWidgets.QApplication(sys.argv)
    MainDialog = MyMainDialog()
    MainDialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    exec()
