'''

@author: orlando.signer@students.unibe.ch
'''

import xlrd
from xml.etree import ElementTree
import re

class MasterPluginGuiCreator(object):
    '''
    This class is responsible to create a GUI from a existing GUI-template and an Excel-File.
    
    You need to have the xlrd-excel plugin installed. To do so, go to libs/xlrd-0.9.2/ and run 'python setup.py install'
    '''
    
    def createPluginGui(self, excelPath, xmlPath, outputPath):
        '''
        This is the main method from this class. It parses the excel and XMl file and creates the XML-GUI to outputPath.
        '''
        excelElements = self.importExcel(excelPath)
        tree = ElementTree.parse(xmlPath)
        widgets = self.getXmlWidgets(tree)
        
        for widget in widgets:
            varId = int(widget.get('name')[-3:])
            if excelElements.has_key(varId):
                self.setWidgetText(widget, excelElements[varId])
            else:
                self.setWidgetInvisible(widget)
        
        tree.write(outputPath)
        
    def setWidgetText(self, widget, text):
        textProp = widget.find("./property[@name='text']")
        if textProp is not None:
            textProp.find("./string").text = text
        
    
    def setWidgetInvisible(self, widget):    
        prop = ElementTree.SubElement(widget, 'property', name='visible')
        boolProp = ElementTree.SubElement(prop, 'bool')
        boolProp.text = 'false'
        
    def importExcel(self, filename):
        '''
        Imports the data from the excel file and returns it as a dictionary where the 
        key is the variable-id and the value is the name for the widget.
        '''
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        guiElements = {}
        for i in range(sheet.nrows):
            if i == 0: 
                continue  # first line contains titles
            row = sheet.row(i)
            varId = round(row[1].value)
            if guiElements.has_key(varId):
                raise ValueError("multiple rows with id (%id)", varId)
            guiElements[varId] = row[4].value
            
        workbook.release_resources()
        return guiElements
    
    def getXmlWidgets(self, tree):
        '''
        Gets all XML-Widgets that we need to manipulate.
        These are the widgets defined in the xml file which name ends with '*_\d{3}'.
        It returns a list with the XML Elements.
        '''
        widgets = []
        self.addChildrenWidgets(tree.find("widget"), widgets)
        return widgets
            
    def addChildrenWidgets(self, widget, children):
        '''
        Recursivly adds all widgets which name ends with '*_\d{3}' to the children list.
        '''
        for child in widget.findall("./"):
            if child.tag == 'widget':
                name = child.get('name')
                regex = re.compile('.*_\d{3}$', flags=re.M)
                if regex.match(name):
                    children.append(child)
                    
            self.addChildrenWidgets(child, children)
