# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IconReduction
                                 A QGIS plugin
 arrange icons in the menubar
                              -------------------
        begin                : 2014-02-27
        copyright            : (C) 2014 by Marc Schneiter
        email                : schneiter@eclipso.ch
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
from iconreductiondialog import IconReductionDialog
import os.path


class IconReduction:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'iconreduction_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = IconReductionDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/iconreduction/icon.png"),
            u"Icon Reduction", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Icon Reduction", self.action)

	# Hide Toolars
	toolbarNames = [
	"mFileToolBar",
	"mLayerToolBar",
	"mDigitizeToolBar",
	"mAdvancedDigitizeToolBar",
	"mMapNavToolBar",
	"mAttributesToolBar",
	"mPluginToolBar",
	"mHelpToolBar",
	"mRasterToolBar",
	"mLabelToolBar",
	"mVectorToolBar",
	"mDatabaseToolBar",
	"mWebToolBar"
	]

	for toolbar in toolbarNames:
		self.iface.mainWindow().findChild(QToolBar,toolbar).setVisible(False)

	# Crate seperate Toolbar
	self.toolbar = self.iface.addToolBar(u"IconReduction");
	self.toolbar.addAction(self.action)

	# Add Tools
	toolNames = [
	"mActionNewProject",
	"mActionSaveProject",
	"mActionDeleteSelected",
	"mActionTouch"
	]
	for tool in toolNames:
		self.toolbar.addAction(self.iface.mainWindow().findChild(QAction,tool))

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Icon Reduction", self.action)
	self.iface.removeToolBarIcon(self.action)

	# Show Toolars
	toolbarNames = [
	"mFileToolBar",
	"mLayerToolBar",
	"mDigitizeToolBar",
	"mAdvancedDigitizeToolBar",
	"mMapNavToolBar",
	"mAttributesToolBar",
	"mPluginToolBar",
	"mHelpToolBar",
	"mRasterToolBar",
	"mLabelToolBar",
	"mVectorToolBar",
	"mDatabaseToolBar",
	"mWebToolBar"
	]

	for toolbar in toolbarNames:
		self.iface.mainWindow().findChild(QToolBar,toolbar).setVisible(True)

    # run method that performs all the real work
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
