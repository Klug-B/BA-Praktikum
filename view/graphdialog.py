# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Plotwidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
# Ui Datei für den Graph

from PyQt5 import QtCore, QtGui
from pyqtgraph import PlotWidget


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
        Dialog.setWindowIcon(QtGui.QIcon("resources/windowicon.png"))
        self.graphwidget = PlotWidget(Dialog)
        self.graphwidget.setGeometry(QtCore.QRect(10, 10, 1150, 750))
        self.graphwidget.setObjectName("graphwidget")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

