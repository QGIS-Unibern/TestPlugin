# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dyngui.ui'
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
from dynguidialog import *
import os.path
# import plugin-functions
from src.SpatiaLiteCreator import createSpatiaLiteDatabase
from src.MasterPluginGuiCreator import createPluginGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dyngui(object):
    def setupUi(self, dyngui):
        dyngui.setObjectName(_fromUtf8("dyngui"))
        dyngui.resize(610, 137)
        self.l_name = QtGui.QLabel(dyngui)
        self.l_name.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self.tl_name = QtGui.QLineEdit(dyngui)
        self.tl_name.setGeometry(QtCore.QRect(140, 10, 461, 27))
        self.tl_name.setObjectName(_fromUtf8("tl_name"))
        self.l_excel = QtGui.QLabel(dyngui)
        self.l_excel.setGeometry(QtCore.QRect(140, 40, 381, 31))
        self.l_excel.setObjectName(_fromUtf8("l_excel"))
        self.l_database = QtGui.QLabel(dyngui)
        self.l_database.setGeometry(QtCore.QRect(140, 70, 381, 31))
        self.l_database.setObjectName(_fromUtf8("l_database"))
        self.b_apply = QtGui.QPushButton(dyngui)
        self.b_apply.setGeometry(QtCore.QRect(500, 100, 101, 27))
        self.b_apply.setObjectName(_fromUtf8("b_apply"))
        self.b_cancel = QtGui.QPushButton(dyngui)
        self.b_cancel.setGeometry(QtCore.QRect(390, 100, 101, 27))
        self.b_cancel.setObjectName(_fromUtf8("b_cancel"))
        self.b_excel = QtGui.QPushButton(dyngui)
        self.b_excel.setGeometry(QtCore.QRect(530, 40, 71, 27))
        self.b_excel.setObjectName(_fromUtf8("b_excel"))
        self.b_database = QtGui.QPushButton(dyngui)
        self.b_database.setGeometry(QtCore.QRect(530, 70, 71, 27))
        self.b_database.setObjectName(_fromUtf8("b_database"))
        self.l_excelText = QtGui.QLabel(dyngui)
        self.l_excelText.setGeometry(QtCore.QRect(10, 40, 121, 31))
        self.l_excelText.setObjectName(_fromUtf8("l_excelText"))
        self.l_databaseText = QtGui.QLabel(dyngui)
        self.l_databaseText.setGeometry(QtCore.QRect(10, 70, 121, 31))
        self.l_databaseText.setObjectName(_fromUtf8("l_databaseText"))

        self.retranslateUi(dyngui)
        QtCore.QMetaObject.connectSlotsByName(dyngui)

        self.connect(self.b_apply, QtCore.SIGNAL("clicked()"), self.apply)
        self.connect(self.b_cancel, QtCore.SIGNAL('clicked()'), self.close)

        self.connect(self.b_excel, QtCore.SIGNAL('clicked()'), self.excel)
        self.connect(self.b_database, QtCore.SIGNAL('clicked()'), self.database)

    def apply(self):
        excel = self.l_excel.text()
        database = self.l_database.text()
        name = self.tl_name.text()
        plugin_dir = os.path.dirname(__file__)
        createSpatiaLiteDatabase(excel, name, database)
        guiName = "%(dir)s/plugin/%(name)s.ui" % {"dir": plugin_dir, "name": name}
        createPluginGui(excel, "%s/res/GuiIteation2.ui"%plugin_dir, guiName)
        self.addLayer(name, database)
        self.close()
        
    def addLayer(self, projectName, projectPath):
        uri = QgsDataSourceURI()
        file = "%s/%s.sqlite" % (projectPath, projectName)
        uri.setDatabase(file)
        schema = ''
        table = projectName
        geom_column = 'Geometry'
        uri.setDataSource(schema, table, geom_column)

        display_name = projectName
        layer = QgsVectorLayer(uri.uri(), display_name, 'spatialite')
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def excel(self):
        read = QFileDialog.getOpenFileName(None ,"Open a Guimask")
        if read and read.strip():
            self.l_excel.setText(read)

    def database(self):
        read = QFileDialog.getExistingDirectory(None ,"Select projectdir")
        if read and read.strip():
            self.l_database.setText(read)

    def retranslateUi(self, dyngui):
        dyngui.setWindowTitle(QtGui.QApplication.translate("dyngui", "dyngui", None, QtGui.QApplication.UnicodeUTF8))
        self.l_name.setText(QtGui.QApplication.translate("dyngui", "Project Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tl_name.setText(QtGui.QApplication.translate("dyngui", "newProject", None, QtGui.QApplication.UnicodeUTF8))
        self.l_excel.setText(QtGui.QApplication.translate("dyngui", "click to choose ...", None, QtGui.QApplication.UnicodeUTF8))
        self.l_database.setText(QtGui.QApplication.translate("dyngui", "click to choose ...", None, QtGui.QApplication.UnicodeUTF8))
        self.b_apply.setText(QtGui.QApplication.translate("dyngui", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.b_cancel.setText(QtGui.QApplication.translate("dyngui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.b_excel.setText(QtGui.QApplication.translate("dyngui", "choose", None, QtGui.QApplication.UnicodeUTF8))
        self.b_database.setText(QtGui.QApplication.translate("dyngui", "choose", None, QtGui.QApplication.UnicodeUTF8))
        self.l_excelText.setText(QtGui.QApplication.translate("dyngui", "Excel-path", None, QtGui.QApplication.UnicodeUTF8))
        self.l_databaseText.setText(QtGui.QApplication.translate("dyngui", "Database-path", None, QtGui.QApplication.UnicodeUTF8))

