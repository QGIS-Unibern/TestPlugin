# -*- coding: utf-8 -*-
"""
/***************************************************************************
 dyngui
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from dynguidialog import dynguiDialog
import os.path
# import plugin-functions
from src.SpatiaLiteCreator import createSpatiaLiteDatabase


class dyngui:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'dyngui_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = dynguiDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/dyngui/icon.png"),
            u"Dynamic Gui", self.iface.mainWindow())
        # Cereate action implementing the info-tool
        self.info = QAction(
            QIcon(":/plugins/dyngui/res/icons/info.png"),
            u"Identify Dynamic Gui", self.iface.mainWindow())
        # Cereate action to load a new Guiform
        self.add = QAction(
            QIcon(":/plugins/dyngui/res/icons/add.png"),
            u"Setup Dynamic Gui", self.iface.mainWindow())
        # connect the actions to methods
        self.action.triggered.connect(self.run)
        self.add.triggered.connect(self.linkGui)

        # Add toolbar button, menu item and info-tool
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Dynamic Gui", self.add)
        self.iface.mainWindow().findChild(QToolBar,"mAttributesToolBar").addAction(self.info)
        # self.info.setDisabled(True)

    def unload(self):
        # Remove the plugin menu item and icons
        self.iface.removePluginMenu(u"&Dynamic Gui", self.add)
        self.iface.removeToolBarIcon(self.action)
        self.iface.mainWindow().findChild(QToolBar,"mAttributesToolBar").removeAction(self.info)

    # run method will open plugin-window
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass

    # this method is called by the add- entry in the menubar
    def linkGui(self):
        fName = QFileDialog.getOpenFileName(None ,"Open a Guimask")
        createSpatiaLiteDatabase(fName, "projectName")
