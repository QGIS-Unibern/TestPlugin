# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_export.ui'
#
# Created: Mon Apr 14 16:18:08 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

# import basic qt-functions
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# imports for filedialogs
from exportdialog import *
import os.path
# import plugin-functions
from src.SpatiaLiteExporter import exportPDF

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_export(object):
    def setupUi(self, export):
        export.setObjectName(_fromUtf8("export"))
        export.resize(610, 137)
        self.l_name = QtGui.QLabel(export)
        self.l_name.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self.tl_name = QtGui.QLineEdit(export)
        self.tl_name.setGeometry(QtCore.QRect(140, 10, 461, 27))
        self.tl_name.setObjectName(_fromUtf8("tl_name"))
        self.l_database = QtGui.QLabel(export)
        self.l_database.setGeometry(QtCore.QRect(140, 40, 381, 31))
        self.l_database.setObjectName(_fromUtf8("l_database"))
        self.l_pdf = QtGui.QLabel(export)
        self.l_pdf.setGeometry(QtCore.QRect(140, 70, 381, 31))
        self.l_pdf.setObjectName(_fromUtf8("l_pdf"))
        self.b_apply = QtGui.QPushButton(export)
        self.b_apply.setGeometry(QtCore.QRect(500, 100, 101, 27))
        self.b_apply.setObjectName(_fromUtf8("b_apply"))
        self.b_cancel = QtGui.QPushButton(export)
        self.b_cancel.setGeometry(QtCore.QRect(390, 100, 101, 27))
        self.b_cancel.setObjectName(_fromUtf8("b_cancel"))
        self.b_database = QtGui.QPushButton(export)
        self.b_database.setGeometry(QtCore.QRect(530, 40, 71, 27))
        self.b_database.setObjectName(_fromUtf8("b_database"))
        self.b_pdf = QtGui.QPushButton(export)
        self.b_pdf.setGeometry(QtCore.QRect(530, 70, 71, 27))
        self.b_pdf.setObjectName(_fromUtf8("b_pdf"))
        self.l_databaseText = QtGui.QLabel(export)
        self.l_databaseText.setGeometry(QtCore.QRect(10, 40, 121, 31))
        self.l_databaseText.setObjectName(_fromUtf8("l_databaseText"))
        self.l_pdfText = QtGui.QLabel(export)
        self.l_pdfText.setGeometry(QtCore.QRect(10, 70, 121, 31))
        self.l_pdfText.setObjectName(_fromUtf8("l_pdfText"))

        self.retranslateUi(export)
        QtCore.QMetaObject.connectSlotsByName(export)

        self.connect(self.b_apply, QtCore.SIGNAL("clicked()"), self.apply)
        self.connect(self.b_cancel, QtCore.SIGNAL('clicked()'), self.close)

        self.connect(self.b_database, QtCore.SIGNAL('clicked()'), self.database)
        self.connect(self.b_pdf, QtCore.SIGNAL('clicked()'), self.pdf)

    def apply(self):
        database = self.l_database.text()
        pdf = self.l_pdf.text()
        name = self.tl_name.text()
        exportPDF(database, "", "", "", pdf + "/" + name + ".pdf");
        self.close()

    def database(self):
        read = QFileDialog.getOpenFileName(None ,"Open a Spatialite-database")
        if read and read.strip():
            self.l_database.setText(read)

    def pdf(self):
        read = QFileDialog.getExistingDirectory(None ,"Select export-directory")
        if read and read.strip():
            self.l_pdf.setText(read)

    def retranslateUi(self, export):
        export.setWindowTitle(QtGui.QApplication.translate("export", "export", None, QtGui.QApplication.UnicodeUTF8))
        self.l_name.setText(QtGui.QApplication.translate("export", "PDF-name", None, QtGui.QApplication.UnicodeUTF8))
        self.tl_name.setText(QtGui.QApplication.translate("export", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.l_database.setText(QtGui.QApplication.translate("export", "click to choose ...", None, QtGui.QApplication.UnicodeUTF8))
        self.l_pdf.setText(QtGui.QApplication.translate("export", "click to choose ...", None, QtGui.QApplication.UnicodeUTF8))
        self.b_apply.setText(QtGui.QApplication.translate("export", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.b_cancel.setText(QtGui.QApplication.translate("export", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.b_database.setText(QtGui.QApplication.translate("export", "choose", None, QtGui.QApplication.UnicodeUTF8))
        self.b_pdf.setText(QtGui.QApplication.translate("export", "choose", None, QtGui.QApplication.UnicodeUTF8))
        self.l_databaseText.setText(QtGui.QApplication.translate("export", "database-path", None, QtGui.QApplication.UnicodeUTF8))
        self.l_pdfText.setText(QtGui.QApplication.translate("export", "Export to", None, QtGui.QApplication.UnicodeUTF8))

