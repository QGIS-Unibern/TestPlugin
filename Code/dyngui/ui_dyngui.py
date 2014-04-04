# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dyngui.ui'
#
# Created: Fri Apr  4 21:50:25 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dyngui(object):
    def setupUi(self, dyngui):
        dyngui.setObjectName(_fromUtf8("dyngui"))
        dyngui.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(dyngui)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(dyngui)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dyngui.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dyngui.reject)
        QtCore.QMetaObject.connectSlotsByName(dyngui)

    def retranslateUi(self, dyngui):
        dyngui.setWindowTitle(QtGui.QApplication.translate("dyngui", "dyngui", None, QtGui.QApplication.UnicodeUTF8))

