# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DynamicGuiLoader
                                 A QGIS plugin
 User-defined gui to represent data
                             -------------------
        begin                : 2014-03-24
        copyright            : (C) 2014 by QgisUnibe - PSE14
        email                : qgis.unibern@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from ui_dyngui import Ui_dyngui
from PyQt4 import QtGui, uic
import sys, os
import os.path
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/reportlab-3.0/src')))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/pyspatialite-2.6.1')))

from pyspatialite import dbapi2 as db


class DynamicGuiLoader(QDialog):

    def __init__(self, guiName, id):
        super(QDialog, self).__init__()
        self.id = id
        self.guiName = guiName
        gui = "%s/plugin/%s.ui" % (os.path.dirname(__file__), guiName)
        self.ui = uic.loadUi(gui, self)
        # Connect the buttons.
        self.connect(self.ui.buttonCancel_1, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.buttonCancel_2, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.buttonSave_1, QtCore.SIGNAL("clicked()"), self.save)
        self.connect(self.ui.buttonSave_2, QtCore.SIGNAL("clicked()"), self.save)

        self.loadData()
        self.exec_()
        
    def loadData(self):
        # TODO hardcoded path
        try:
            conn = db.connect("/home/orlandopse/newProject.sqlite")
            cur = conn.cursor()
            self.constData = self.getConstData(cur)
            self.varIds = self.getVarIds(cur)
            self.varId = self.varIds[-1]
            self.varData = self.getVarData(cur)
            print(self.varData)
        finally:
            if conn:
                conn.close()
        
        self.widgets = self.ui.findChildren((QtGui.QLineEdit, QtGui.QCheckBox, QtGui.QComboBox))
        self.setDataToGui(self.constData)
        self.setDataToGui(self.varData)
    
    def save(self):
        self.setDataToMap(self.constData)
        self.setDataToMap(self.varData)
                
        # TODO hardcoded path
        try:
            conn = db.connect("/home/orlandopse/newProject.sqlite")
            cur = conn.cursor()
            
            sql = "UPDATE %s SET " % self.guiName
            for key, value in self.constData.iteritems():
                if key == 'geometry' or key == 'id':
                    continue
                sql += "'%s' = '%s'," % (key.replace('_', ' '), value)
            sql = sql[:-1]  # remove last comma
            sql += " WHERE id = %s;" % self.id
            cur.execute(sql)
            
            sql = "UPDATE %s SET " % (self.guiName + '_var')
            for key, value in self.varData.iteritems():
                if key == 'geometry' or key == 'id' or key == 'parent_id':
                    continue
                if value is None:
                    value = ''
                sql += "'%s' = '%s'," % (key.replace('_', ' '), value)
            sql = sql[:-1]
            sql += " WHERE id = %s" % self.varId
            sql += " AND parent_id = %s" % self.id
            cur.execute(sql)
            conn.commit()
        finally:
            if conn:
                conn.close()

    def setDataToGui(self, data):
        for key, value in data.iteritems():
            for widget in self.widgets:
                widgetName = str(widget.objectName())
                if widgetName.endswith(key):
                    if type(widget) is QtGui.QLineEdit:
                        widget.setText(value)
                    elif type(widget) is QtGui.QCheckBox:
                        widget.setChecked(value == 'True')
                    elif type(widget) is QtGui.QComboBox:
                        pass
                    break
    
    def setDataToMap(self, data):
        for key in data:
            for widget in self.widgets:
                widgetName = str(widget.objectName())
                if widgetName.endswith(key):
                    if type(widget) is QtGui.QLineEdit:
                        data[key] = str(widget.text())
                    elif type(widget) is QtGui.QCheckBox:
                        data[key] = widget.isChecked()
                    elif type(widget) is QtGui.QComboBox:
                        pass
                    break
        
        
    def cancel(self):
        self.close()
        
    def getConstData(self, cursor):
        sql = "SELECT * FROM %s WHERE id = ?;" % self.guiName
        cursor.execute(sql, (self.id))
        data = cursor.fetchall()
        map = self.matchDataWithColumnNames(cursor, data[0], self.guiName)
        return map
    
    def getVarIds(self, cursor):
        sql = "SELECT id FROM %s WHERE parent_id = ?;" % (self.guiName + "_var")
        cursor.execute(sql, (self.id))
        data = cursor.fetchall()
        return data[0]

    def getVarData(self, cursor):
        sql = "SELECT * FROM %s WHERE id = ? AND parent_id = ?;" % (self.guiName + "_var")
        cursor.execute(sql, (self.varId, self.id))
        data = cursor.fetchall()
        # keine daten vorhanden --> neuen Datensatz erstellen
        if len(data) <= 0:
            self.createNewVarData(cursor)
            return self.getVarData(cursor)

        map = self.matchDataWithColumnNames(cursor, data[0], self.guiName + "_var")
        return map
    
    def matchDataWithColumnNames(self, cursor, data, tableName):
        if not data:
            return {}
        sql = "PRAGMA table_info(%s);" % tableName 
        cursor.execute(sql)
        names = cursor.fetchall()
        map = {}
        for name in names:
            n = name[1].replace(' ', '_')
            map[n] =  data[name[0]]
        return map
    
    def createNewVarData(self, cursor):
        sql = "INSERT INTO %s (parent_id) " % (self.guiName + '_var')
        sql += "VALUES (%s);" % self.id
        cursor.execute(sql)
        self.varIds = self.getVarIds(cursor)
        self.varId = self.varIds[-1]
        
