# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_export.ui'
#
# Created: Mon Apr 14 16:18:08 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

# import basic qt-functions & stuff
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import numpy as np
# imports for filedialogs
from exportdialog import *
import os.path
# import plugin-functions
from src.SpatiaLiteExporter import *
# prepateimport from library
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, './libs/pyspatialite-2.6.1')))
# import database-module
from pyspatialite import dbapi2 as db

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_export(object):
    def setValues(self, parDbPath, parProjectName, parObjectIDs):
        self.dbPath = parDbPath
        self.projectName = parProjectName
        self.objectIDs = np.asarray(parObjectIDs)
        conn = db.connect(self.dbPath)
        cur = conn.cursor()
        self.treeConstants.clear()
        self.treeVariables.clear()
        self.addItems(self.treeConstants, getConstAttributes(cur, self.projectName))
        self.addItems(self.treeVariables, getVarAttributes(cur, self.projectName))

    def setupUi(self, export):
        export.setObjectName(_fromUtf8("export"))
        export.resize(610, 530)
        self.l_name = QtGui.QLabel(export)
        self.l_name.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self.tl_name = QtGui.QLineEdit(export)
        self.tl_name.setGeometry(QtCore.QRect(140, 10, 461, 27))
        self.tl_name.setObjectName(_fromUtf8("tl_name"))
        self.l_pdf = QtGui.QLabel(export)
        self.l_pdf.setGeometry(QtCore.QRect(140, 40, 381, 31))
        self.l_pdf.setObjectName(_fromUtf8("l_pdf"))
        self.b_apply = QtGui.QPushButton(export)
        self.b_apply.setGeometry(QtCore.QRect(500, 495, 101, 27))
        self.b_apply.setObjectName(_fromUtf8("b_apply"))
        self.b_cancel = QtGui.QPushButton(export)
        self.b_cancel.setGeometry(QtCore.QRect(390, 495, 101, 27))
        self.b_cancel.setObjectName(_fromUtf8("b_cancel"))
        self.b_pdf = QtGui.QPushButton(export)
        self.b_pdf.setGeometry(QtCore.QRect(530, 40, 71, 27))
        self.b_pdf.setObjectName(_fromUtf8("b_pdf"))
        self.l_pdfText = QtGui.QLabel(export)
        self.l_pdfText.setGeometry(QtCore.QRect(10, 40, 121, 31))
        self.l_pdfText.setObjectName(_fromUtf8("l_pdfText"))
        self.treeConstants = QtGui.QTreeWidget(export)
        self.treeConstants.setGeometry(QtCore.QRect(10, 80, 585, 200))
        self.treeConstants.setObjectName(_fromUtf8("treeConstants"))
        self.treeConstants.setHeaderLabel("Constants")
        self.treeVariables = QtGui.QTreeWidget(export)
        self.treeVariables.setGeometry(QtCore.QRect(10, 285, 585, 200))
        self.treeVariables.setObjectName(_fromUtf8("treeVariables"))
        self.treeVariables.setHeaderLabel("Variables")

        self.retranslateUi(export)
        QtCore.QMetaObject.connectSlotsByName(export)

        self.connect(self.b_apply, QtCore.SIGNAL("clicked()"), self.apply)
        self.connect(self.b_cancel, QtCore.SIGNAL('clicked()'), self.close)
        self.connect(self.b_pdf, QtCore.SIGNAL('clicked()'), self.pdf)

    def apply(self):
        # get values from input
        pdf = self.l_pdf.text()
        name = self.tl_name.text()

        # read checked items
        constants = []
        variables = []
        root = self.treeConstants.invisibleRootItem()
        for i in range(root.childCount()):
            if root.child(i).checkState(0) == QtCore.Qt.Checked:
                constants.append(root.child(i).text(0))
        root = self.treeVariables.invisibleRootItem()
        for i in range(root.childCount()):
            if root.child(i).checkState(0) == QtCore.Qt.Checked:
                variables.append(root.child(i).text(0))

        # call export-method
        exportPDF(self.dbPath, self.projectName, self.objectIDs, [constants, variables], pdf + "/" + name + ".pdf");
        self.close()

    def pdf(self):
        read = QFileDialog.getExistingDirectory(None ,"Select exportdir")
        if read and read.strip():
            self.l_pdf.setText(read)

    def addItems(self, p,ch):
        if isinstance(ch,dict):
            for k,v in ch.iteritems():
                item = QTreeWidgetItem(p)
                item.setText(0, k)
                item.setCheckState(0, Qt.Checked)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.addItems(item,v)
        else:
            for txt in ch:
                item = QTreeWidgetItem(p)
                item.setText(0, txt)
                item.setCheckState(0, Qt.Checked)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

    def retranslateUi(self, export):
        export.setWindowTitle(QtGui.QApplication.translate("export", "export", None, QtGui.QApplication.UnicodeUTF8))
        self.l_name.setText(QtGui.QApplication.translate("export", "PDF-name", None, QtGui.QApplication.UnicodeUTF8))
        self.tl_name.setText(QtGui.QApplication.translate("export", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.l_pdf.setText(QtGui.QApplication.translate("export", "click to choose ...", None, QtGui.QApplication.UnicodeUTF8))
        self.b_apply.setText(QtGui.QApplication.translate("export", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.b_cancel.setText(QtGui.QApplication.translate("export", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.b_pdf.setText(QtGui.QApplication.translate("export", "choose", None, QtGui.QApplication.UnicodeUTF8))
        self.l_pdfText.setText(QtGui.QApplication.translate("export", "Export to", None, QtGui.QApplication.UnicodeUTF8))
