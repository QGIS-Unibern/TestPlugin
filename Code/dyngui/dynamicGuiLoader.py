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

    '''
    Initializes the GUI and sets the data from the database.
    '''
    def __init__(self, guiName, id):
        super(QDialog, self).__init__()
        self.id = id
        self.guiName = guiName
        gui = "%s/plugin/%s.ui" % (os.path.dirname(__file__), guiName)
        self.ui = uic.loadUi(gui, self)
        self.widgets = self.ui.findChildren((QtGui.QLineEdit, QtGui.QCheckBox, QtGui.QComboBox))
        # Connect the buttons.
        self.connect(self.ui.buttonCancel_1, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.buttonCancel_2, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.buttonSave_1, QtCore.SIGNAL("clicked()"), self.save)
        self.connect(self.ui.buttonSave_2, QtCore.SIGNAL("clicked()"), self.save)
        self.connect(self.ui.buttonPreviousData, QtCore.SIGNAL("clicked()"), self.previousVarData)
        self.connect(self.ui.buttonNextData, QtCore.SIGNAL("clicked()"), self.nextVarData)
        self.connect(self.ui.buttonNewData, QtCore.SIGNAL("clicked()"), self.newVarData)

        try:
            conn = self.getDbConnection()
            cur = conn.cursor()
            self.loadConstData(cur)
            
            self.varIds = self.getVarIds(cur)
            if len(self.varIds) > 0:
                self.varId = self.varIds[-1]
            else:
                self.varId = 0
            self.loadVarData(cur)
        finally:
            if conn:
                conn.commit()
                conn.close()
        
        self.exec_()
        
    def getDbConnection(self):
        # TODO hardcoded path
        return db.connect("/home/orlandopse/newProject.sqlite")
    
    '''
    Loads the constant data from the database and sets it into the 'Konstante Daten'-Tab 
    '''
    def loadConstData(self, cursor):
        self.constData = self.getConstData(cursor)
        self.setDataToGui(self.constData)
    '''
    Loads the variable data from the database and sets it into the 'Variable Daten'-Tab.
    It loads the var data with the id set in self.varId 
    '''
    def loadVarData(self, cursor):
        self.varData = self.getVarData(cursor)
        self.setDataToGui(self.varData)

    '''
    Action from the Speichern-Button. Stores the value from the GUI to the database.
    '''
    def save(self):
        self.setDataToMap(self.constData)
        self.setDataToMap(self.varData)
                
        try:
            conn = self.getDbConnection()
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
    '''
    Action from the Vorwärts-Button. Sets the next variable data.
    '''
    def nextVarData(self):
        print(self.varIds)
        print(self.varId)
        index = self.varIds.index(self.varId)
        if index < len(self.varIds) - 1:
            index += 1
        else:
            index = len(self.varIds) - 1
        self.varId = self.varIds[index]
        
        try:
            conn = self.getDbConnection()
            cursor = conn.cursor()
            self.loadVarData(cursor)
        finally:
            if conn:
                conn.close()
    
    '''
    Action from the Zurück-Button. Sets the previous variable data.
    '''
    def previousVarData(self):
        index = self.varIds.index(self.varId)
        if index > 0:
            index -= 1
        else:
            index = 0
        self.varId = self.varIds[index]
        
        try:
            conn = self.getDbConnection()
            cursor = conn.cursor()
            self.loadVarData(cursor)
        finally:
            if conn:
                conn.close()
    
    '''
    Action from the 'Zeitpunkt hinzufügen'-Button. Adds a new, empty VarData entry.
    '''
    def newVarData(self):
        try:
            conn = self.getDbConnection()
            cursor = conn.cursor()
            self.createNewVarData(cursor)
            self.loadVarData(cursor)
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
        
    '''
    Gets the constant data from the database.
    They are stored in a map with the column-name as key and the actual value as value
    '''
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
        data = [i[0] for i in data]
        return data

    '''
    Gets the variable data from the database.
    They are stored in a map with the column-name as key and the actual value as value
    '''
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
    
    '''
    Create a new Var Data entry in the database.
    Only the id and parent_id are set.
    '''
    def createNewVarData(self, cursor):
        sql = "INSERT INTO %s (parent_id) " % (self.guiName + '_var')
        sql += "VALUES (%s);" % self.id
        cursor.execute(sql)
        self.varIds = self.getVarIds(cursor)
        self.varId = self.varIds[-1]
        
