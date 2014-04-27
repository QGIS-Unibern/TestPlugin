from PyQt4.Qt import QMessageBox
from qgis.gui import QgsMapToolIdentify
from qgis.gui import QgsMapTool
from qgis.core import QgsRectangle
from PyQt4 import QtCore, QtGui, uic
from dynamicGuiLoader import DynamicGuiLoader

"""
/***************************************************************************
 InfoPointTool
                                 A QGIS plugin
 A QgsMapTool that identifies the user selected feature and opens the right dyamic gui.
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
class InfoPointTool(QgsMapTool):   
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas    
        
    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        
        # Ugly hack to identify the clicked element. For some reasons if InfoPointTool inherits from QgsMapToolIdentify,
        # canvasRealeaseEvent isn't called.
        tool = QgsMapToolIdentify(self.canvas)
        results = tool.identify(x,y, tool.ActiveLayer, tool.AllLayers)
        if not results:
            return
        
        guiName = self.canvas.currentLayer().name()
        
        result = results[0]
        
        feat = result.mFeature
        attrs = feat.attributes()
        fields = feat.fields().toList()
        
        for i, attr in enumerate(attrs):
            name = fields[i].name()
            if name == 'id':
                id = str(attr)
                break

        DynamicGuiLoader(guiName, id)
    
