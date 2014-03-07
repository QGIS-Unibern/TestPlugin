# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_iconreduction.ui'
#
# Created: Sat Mar  1 13:18:50 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_IconReduction(object):
    def setupUi(self, IconReduction):
        IconReduction.setObjectName(_fromUtf8("IconReduction"))
        IconReduction.resize(323, 270)
        self.treeWidget = QtGui.QTreeWidget(IconReduction)
        self.treeWidget.setGeometry(QtCore.QRect(10, 40, 301, 181))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        self.B_Apply = QtGui.QPushButton(IconReduction)
        self.B_Apply.setGeometry(QtCore.QRect(10, 230, 301, 27))
        self.B_Apply.setObjectName(_fromUtf8("B_Apply"))
        self.listWidget = QtGui.QListWidget(IconReduction)
        self.listWidget.setGeometry(QtCore.QRect(60, 10, 251, 21))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.B_Apply_2 = QtGui.QPushButton(IconReduction)
        self.B_Apply_2.setGeometry(QtCore.QRect(10, 10, 21, 21))
        self.B_Apply_2.setObjectName(_fromUtf8("B_Apply_2"))
        self.B_Apply_3 = QtGui.QPushButton(IconReduction)
        self.B_Apply_3.setGeometry(QtCore.QRect(30, 10, 21, 21))
        self.B_Apply_3.setObjectName(_fromUtf8("B_Apply_3"))

        self.retranslateUi(IconReduction)
        QtCore.QMetaObject.connectSlotsByName(IconReduction)

    def retranslateUi(self, IconReduction):
        IconReduction.setWindowTitle(QtGui.QApplication.translate("IconReduction", "IconReduction", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("IconReduction", "ToolBar 1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("IconReduction", "Tool 1.1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("IconReduction", "Tool 1.2", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(1).setText(0, QtGui.QApplication.translate("IconReduction", "ToolBar 2", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(1).child(0).setText(0, QtGui.QApplication.translate("IconReduction", "Tool 2.1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(1).child(1).setText(0, QtGui.QApplication.translate("IconReduction", "Tool 2.2", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(1).child(2).setText(0, QtGui.QApplication.translate("IconReduction", "Tool 2.3", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(2).setText(0, QtGui.QApplication.translate("IconReduction", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.B_Apply.setText(QtGui.QApplication.translate("IconReduction", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(QtGui.QApplication.translate("IconReduction", "CustomView 1", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(1)
        item.setText(QtGui.QApplication.translate("IconReduction", "CustomView 2", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(2)
        item.setText(QtGui.QApplication.translate("IconReduction", "CustomView 3", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.B_Apply_2.setText(QtGui.QApplication.translate("IconReduction", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.B_Apply_3.setText(QtGui.QApplication.translate("IconReduction", "-", None, QtGui.QApplication.UnicodeUTF8))

