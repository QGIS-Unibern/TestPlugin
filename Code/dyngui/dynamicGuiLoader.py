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
# create the dialog for zoom to point


class DynamicGuiLoader(QDialog):
    def __init__(self, guiName):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi(guiName, self)
        # Connect up the buttons.
        self.connect(self.ui.okButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()"))
        self.connect(self.ui.cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))

        self.exec_()
        
    def accept(self):
        print("accept")
        super.accept()
