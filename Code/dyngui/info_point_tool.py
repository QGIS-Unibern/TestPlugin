from PyQt4.Qt import QMessageBox
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

    def canvasPressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        layer = self.iface.activeLayer()
        DynamicGuiLoader(self.guiName)
        
    def canvasMoveEvent(self, event):
        pass
       

    def canvasReleaseEvent(self, event):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True