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

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QFileDialog
from ui_dyngui import Ui_dyngui
import sys, os
import subprocess
import os.path
import functools
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/reportlab-3.0/src')))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/pyspatialite-2.6.1')))

from pyspatialite import dbapi2 as db


class DynamicGuiLoader(QDialog):

    '''
    Initializes the GUI and sets the data from the database.
    '''
    def __init__(self, dbName, guiName, id):
        super(QDialog, self).__init__()
        self.dbName = dbName
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
        self.connect(self.ui.buttonDeleteData, QtCore.SIGNAL("clicked()"), self.deleteVarData)
        # Buttons for open/add/delete files
        self.connect(self.ui.button_open_photo_var, QtCore.SIGNAL("clicked()"), functools.partial(self.openFile, True, True))
        self.connect(self.ui.button_open_photo, QtCore.SIGNAL("clicked()"), functools.partial(self.openFile, True, False))
        self.connect(self.ui.button_open_doc_var, QtCore.SIGNAL("clicked()"), functools.partial(self.openFile, False, True))
        self.connect(self.ui.button_open_doc, QtCore.SIGNAL("clicked()"), functools.partial(self.openFile, False, False))
        self.connect(self.ui.button_add_photo_var, QtCore.SIGNAL("clicked()"), functools.partial(self.addFile, True, True))
        self.connect(self.ui.button_add_photo, QtCore.SIGNAL("clicked()"), functools.partial(self.addFile, True, False))
        self.connect(self.ui.button_add_doc_var, QtCore.SIGNAL("clicked()"), functools.partial(self.addFile, False, True))
        self.connect(self.ui.button_add_doc, QtCore.SIGNAL("clicked()"), functools.partial(self.addFile, False, False))
        self.connect(self.ui.button_delete_photo_var, QtCore.SIGNAL("clicked()"), functools.partial(self.removeFile, True, True))
        self.connect(self.ui.button_delete_photo, QtCore.SIGNAL("clicked()"), functools.partial(self.removeFile, True, False))
        self.connect(self.ui.button_delete_doc_var, QtCore.SIGNAL("clicked()"), functools.partial(self.removeFile, False, True))
        self.connect(self.ui.button_delete_doc, QtCore.SIGNAL("clicked()"), functools.partial(self.removeFile, False, False))
        
        self.listWidget_photo_var.itemDoubleClicked.connect(functools.partial(self.openFile, True, True))
        self.listWidget_photo.itemDoubleClicked.connect(functools.partial(self.openFile, True, False))
        self.listWidget_doc_var.itemDoubleClicked.connect(functools.partial(self.openFile, False, True))
        self.listWidget_doc.itemDoubleClicked.connect(functools.partial(self.openFile, False, False))


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
            
            self.loadFileData(cur, False)
        finally:
            if conn:
                conn.commit()
                conn.close()
        
        self.exec_()
        
    '''
    Evaluates the selected file from the correct file-ListWidget and opens with the default application
    '''
    def openFile(self, isPhoto, isVar):
        view = self.getFileListWidget(isPhoto, isVar)
        if view.currentRow() >= 0:
            file = view.currentItem().text()
            # see http://stackoverflow.com/a/435669
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', file))
            elif os.name == 'nt':
                os.startfile(file)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', file))
        
    def addFile(self, isPhoto, isVar):
        fileTypes = ""
        if isPhoto:
            fileTypes = "Bilder (*.jpg *.jpeg *.png *.gif *.bmp *.tiff)"
        read = QFileDialog.getOpenFileName(self ,"Datei auswählen", filter=fileTypes)
        
        if read and read.strip():
            view = self.getFileListWidget(isPhoto, isVar)
            if not view.findItems(read, QtCore.Qt.MatchExactly):
                view.addItem(read)
                self.persistFile(read, isPhoto, isVar)
    
    def persistFile(self, filename, isPhoto, isVar):
        tblName = self.getFileTableName(isPhoto, isVar)
        dataId = self.varId if isVar else self.id
        sql = "INSERT INTO %s (ref_id, path) "
        sql += "VALUES (?, ?)"
        sql = sql % tblName
        
        try:
            conn = self.getDbConnection()
            cur = conn.cursor()
            cur.execute(sql, (dataId, filename))
        finally:
            if conn:
                conn.commit()
                conn.close()      
        
    def removeFile(self, isPhoto, isVar):
        view = self.getFileListWidget(isPhoto, isVar)
        if view.currentRow() >= 0:
            item = view.takeItem(view.currentRow())
            self.deleteFile(item.text(), isPhoto, isVar)
            
    def deleteFile(self, filename, isPhoto, isVar):
        tblName = self.getFileTableName(isPhoto, isVar)
        dataId = self.varId if isVar else self.id
        sql = "DELETE FROM %s "
        sql += "WHERE ref_id = ? AND path = ?"
        sql = sql % tblName
        try:
            conn = self.getDbConnection()
            cur = conn.cursor()
            cur.execute(sql, (dataId, filename))
        finally:
            if conn:
                conn.commit()
                conn.close()

        
    def getFileListWidget(self, isPhoto, isVar):
        if isPhoto:
            if isVar:
                return self.ui.listWidget_photo_var
            else: 
                return self.ui.listWidget_photo
        else:
            if isVar:
               return self.ui.listWidget_doc_var
            else:
                return self.ui.listWidget_doc
    
    def getDbConnection(self):
        return db.connect(self.dbName)
    
    def getFileTableName(self, isPhoto, isVar):
        type = "fotos" if isPhoto else "doc"
        var = "var" if isVar else "const"
        return "%s_%s_%s " % (self.guiName, type, var)
    
    def loadFileData(self, cursor, isVar):
        vals = [True, False]
        for isPhoto in vals:
            widget = self.getFileListWidget(isPhoto, isVar)
            widget.clear()
            result = self.loadFileData2(cursor, isPhoto, isVar)
            for data in result:
                widget.addItem(data)
    
    def loadFileData2(self, cursor, isPhoto, isVar):
        dataId = self.varId if isVar else self.id
        table = self.getFileTableName(isPhoto, isVar)
        sql = "SELECT path FROM %s "
        sql += "WHERE ref_id = ?"
        sql = sql % table
        cursor.execute(sql, [str(dataId)])
        data = cursor.fetchall()
        data = [i[0] for i in data]
        return data
        
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
        self.loadFileData(cursor, True)
        self.updateCountLabel()

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
            sql = sql[:-1]  # removeFile last comma
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
                
    def deleteVarData(self):
        if (len(self.varIds) <= 1):
            return
        try:
            conn = self.getDbConnection()
            cursor = conn.cursor()
            
            sql = "DELETE FROM %s WHERE id = ?" % (self.guiName + '_var')
            cursor.execute(sql, [self.varId])
                        
            prevIndex = self.varIds.index(self.varId) - 1
            if prevIndex < 0:
                prevIndex = 0
            self.varId = self.varIds[prevIndex]
            self.varIds = self.getVarIds(cursor)
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
                        for i in range(widget.count()):
                            if widget.itemText(i) == value:
                                widget.setCurrentIndex(i)
                                break
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
                        data[key] = str(widget.currentText())
                    break
    
    def updateCountLabel(self):
        index = self.varIds.index(self.varId) + 1
        total = len(self.varIds)
        txt = "%d/%d" % (index, total)
        self.ui.lblEventCount.setText(txt)
        
        
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
            map[n] = data[name[0]]
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
        
