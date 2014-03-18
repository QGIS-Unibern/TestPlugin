'''

@author: orlando.signer@students.unibe.ch
'''

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
            setWidgetText(widget, excelElements[varId])
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
