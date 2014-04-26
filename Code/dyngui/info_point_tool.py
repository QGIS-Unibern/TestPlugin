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
        results = tool.identify(x,y, tool. TopDownStopAtFirst, tool.AllLayers)
        if not results:
            return
        result = results[0]
        print(result)
        print(result.mFeature.attributes())
        print(result.mFeature.fields())
        print(result.mDerivedAttributes)
        print("Fields")
        for f in result.mFeature.fields().toList():
            print(f)
            print(f.name())
        print("________________")
        
        # hard coded plugin name, replace it!
        guiName = "/home/orlandopse/newProject.ui"
        DynamicGuiLoader(guiName)
    
