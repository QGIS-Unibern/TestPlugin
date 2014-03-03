# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_testplugin.ui'
#
# Created: Sat Feb 22 23:34:56 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TestPlugin(object):
    def setupUi(self, TestPlugin):
        TestPlugin.setObjectName(_fromUtf8("TestPlugin"))
        TestPlugin.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(TestPlugin)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(TestPlugin)
        self.label.setGeometry(QtCore.QRect(170, 90, 171, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(TestPlugin)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TestPlugin.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TestPlugin.reject)
        QtCore.QMetaObject.connectSlotsByName(TestPlugin)

    def retranslateUi(self, TestPlugin):
        TestPlugin.setWindowTitle(_translate("TestPlugin", "TestPlugin", None))
        self.label.setText(_translate("TestPlugin", "Hello World12345", None))

