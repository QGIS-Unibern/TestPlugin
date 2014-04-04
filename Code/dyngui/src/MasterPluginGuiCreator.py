'''

@author: orlando.signer@students.unibe.ch
'''
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/xlrd-0.9.2')))

import xlrd
from xml.etree import ElementTree
import re

def createPluginGui(excelPath, xmlPath, outputPath):
    '''
    This is the main method from this class. It parses the excel and XMl file and creates the XML-GUI to outputPath.
    '''
    excelElements = importExcel(excelPath)
    tree = ElementTree.parse(xmlPath)
    widgets = getXmlWidgets(tree)
    
    for widget in widgets:
        varId = int(widget.get('name')[-3:])
        if excelElements.has_key(varId):
            setWidgetText(widget, excelElements[varId].name)
        else:
            setWidgetInvisible(widget)
    
    tree.write(outputPath)
    
def setWidgetText(widget, text):
    textProp = widget.find("./property[@name='text']")
    if textProp is not None:
        textProp.find("./string").text = text
    

def setWidgetInvisible(widget):    
    prop = ElementTree.SubElement(widget, 'property', name='visible')
    boolProp = ElementTree.SubElement(prop, 'bool')
    boolProp.text = 'false'
    
def importExcel(filename):
    '''
    Imports the data from the excel file and returns it as a dictionary of ExcelRows. The varId is the key for the ExcelRow.
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
        
        isVariabel = row[3].value.count('variabel') > 0
        name = row[4].value
        guiElements[varId] = ExcelRow(varId, name, isVariabel)
        
    workbook.release_resources()
    return guiElements

def getXmlWidgets(tree):
    '''
    Gets all XML-Widgets that we need to manipulate.
    These are the widgets defined in the xml file which name ends with '*_\d{3}'.
    It returns a list with the XML Elements.
    '''
    widgets = []
    addChildrenWidgets(tree.find("widget"), widgets)
    return widgets
        
def addChildrenWidgets(widget, children):
    '''
    Recursivly adds all widgets which name ends with '*_\d{3}' to the children list.
    '''
    for child in widget.findall("./"):
        if child.tag == 'widget':
            name = child.get('name')
            regex = re.compile('.*_\d{3}$', flags=re.M)
            if regex.match(name):
                children.append(child)
                
        addChildrenWidgets(child, children)

class ExcelRow(object):
    def __init__(self, varId, name, isVariabel):
        self.varId = varId
        self.name = name
        self.isVariabel = isVariabel
