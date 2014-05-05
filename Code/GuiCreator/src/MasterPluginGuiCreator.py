'''

@author: orlando.signer@students.unibe.ch
'''

import xlrd
from xml.etree import ElementTree
import re

'''
This is the main method from this class. It parses the excel and XMl file and creates the XML-GUI to outputPath.
''' 
def createPluginGui(excelPath, xmlPath, outputPath):
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
    
def setWidgetText(widget, element):
    textProp = widget.find("./property[@name='text']")
    if textProp is not None:
        textProp.find("./string").text = element.name
    name = widget.get('name')
    name = name.split('_')[0] + ('_' + element.name.replace(' ', '_'))
    widget.set('name', name)
    if element.fieldType == 'combobox':
        # TODO add combobox items
        pass
    

def setWidgetInvisible(widget):    
    prop = ElementTree.SubElement(widget, 'property', name='visible')
    boolProp = ElementTree.SubElement(prop, 'bool')
    boolProp.text = 'false'

'''
Imports the data from the excel file and returns it as a dictionary of ExcelRows. The varId is the key for the ExcelRow.
'''
def importExcel(filename):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    guiElements = {}
    for i in range(sheet.nrows):
        if i == 0: 
            continue  # first line contains titles
        row = sheet.row(i)
        varId = round(row[0].value)
        if guiElements.has_key(varId):
            raise ValueError("multiple rows with id (%id)", varId)
        
        isVariabel = row[1].value.count('variabel') > 0
        name = row[2].value
        fieldType = row[3].value
        comboItems = []
        if fieldType and fieldType.lower() == 'combobox':
            index = 4
            val = row[index]
            while index <= len(row) - 1:
                val = row[index]
                comboItems.append(val)
                index += 1
        guiElements[varId] = ExcelRow(varId, name, isVariabel, fieldType, comboItems)
        
    workbook.release_resources()
    return guiElements

'''
Gets all XML-Widgets that we need to manipulate.
These are the widgets defined in the xml file which name ends with '*_\d{3}'.
It returns a list with the XML Elements.
'''
def getXmlWidgets(tree):
    widgets = []
    addChildrenWidgets(tree.find("widget"), widgets)
    return widgets
        
'''
Recursivly adds all widgets which name ends with '*_\d{3}' to the children list.
'''
def addChildrenWidgets(widget, children):
    regex = re.compile('.*_\d{3}$', flags=re.M)
    for child in widget.findall("./"):
        if child.tag == 'widget':
            name = child.get('name')
            if regex.match(name):
                children.append(child) 
        addChildrenWidgets(child, children)

class ExcelRow(object):
    def __init__(self, varId, name, isVariabel, fieldType, comboItems):
        self.varId = varId
        self.name = name
        self.isVariabel = isVariabel
        self.fieldType = fieldType.lower()
        self.comboItems = comboItems
