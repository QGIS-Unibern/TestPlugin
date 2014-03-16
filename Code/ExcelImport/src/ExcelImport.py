'''

@author: orlando.signer@students.unibe.ch
'''

import xlrd
from xml.etree import ElementTree
import re

class ExcelImport(object):
    '''
    classdocs
    '''
    
    def __init__(self, ):
        '''
        Constructor
        '''
        
    def createPluginGui(self, excelPath, xmlPath, outputPath):
        excelElements = self.importExcel(excelPath)
        tree = ElementTree.parse(xmlPath)
        widgets = self.getXmlWidgets(tree)
        
        print widgets
        
        for widget in widgets:
            id = int(widget.get('name')[-3:])
            name = excelElements[id]
            if name is None:
                print 'id: {0} is none'.format(id)
            else:
                textProp = widget.find("./property[@name='text']")
                if textProp is not None:
                    textProp.find("./string").text = name
        
        tree.write(outputPath)
        
        
        
    def importExcel(self, filename):
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        guiElements = {}
        for i in range(sheet.nrows):
            if i == 0: 
                continue # first line contains titles
            row = sheet.row(i)
            varId = round(row[1].value)
            if guiElements.has_key(varId):
                raise ValueError("multiple rows with id (%id)", varId)
            guiElements[varId] = row[4].value
            
        workbook.release_resources()
        return guiElements
    
    def getXmlWidgets(self, tree):
        widgets = []
        self.addChildrenWidgets(tree.find("widget"), widgets)
        return widgets
            
    def addChildrenWidgets(self, widget, children):
        for child in widget.findall("./"):
            if child.tag == 'widget':
                name = child.get('name')
                regex = re.compile('.*_\d{3}$', flags=re.M)
                if regex.match(name):
                    children.append(child)
                    
            self.addChildrenWidgets(child, children)