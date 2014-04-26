# -*- coding: utf-8 -*-
"""
/***************************************************************************
 dynguiDialog
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
import os.path


class DynamicGuiLoader(QDialog):
    def __init__(self, guiName, id):
        super(QDialog, self).__init__()
        gui = "%s/plugin/%s.ui" % (os.path.dirname(__file__), guiName)
        self.id = id
        self.ui = uic.loadUi(gui, self)
        # Connect the buttons.
        self.connect(self.ui.buttonCancel_1, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.buttonCancel_2, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.buttonSave_1, QtCore.SIGNAL("clicked()"), self.save)
        self.connect(self.ui.buttonSave_2, QtCore.SIGNAL("clicked()"), self.save)

        self.exec_()
        self.loadData()
        
    def loadData(self):
        print(self.id)
        
    def save(self):
        print("save")
        
    def cancel(self):
        print("cancel")
