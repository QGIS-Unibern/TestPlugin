from PyQt4.Qt import QMessageBox
from qgis.gui import QgsMapToolIdentify
from qgis.gui import QgsMapTool
from qgis.core import QgsRectangle
from PyQt4 import QtCore, QtGui, uic
from dynamicGuiLoader import DynamicGuiLoader


class InfoPointTool(QgsMapTool):   
    def __init__(self, canvas, iface, guiName):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas    
        self.iface = iface
        self.guiName = guiName
        
    def identify(self, *args, **kwargs):
        print("identifiying")
        return QgsMapToolIdentify.identify(self, *args, **kwargs)

    def canvasPressEvent(self, event):
        print("press")
        pass
        
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        print("released")
        x = event.pos().x()
        y = event.pos().y()
        
        tool = QgsMapToolIdentify(self.canvas)
        results = tool.identify(x,y, tool.TopDownStopAtFirst, tool.VectorLayer)

        DynamicGuiLoader(self.guiName)
    
