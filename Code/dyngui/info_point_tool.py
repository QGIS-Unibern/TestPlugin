from PyQt4.Qt import QMessageBox
from qgis.gui import QgsMapToolIdentify
from qgis.gui import QgsMapTool
from qgis.core import QgsRectangle
from PyQt4 import QtCore, QtGui, uic
from dynamicGuiLoader import DynamicGuiLoader


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
    
