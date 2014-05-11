'''
Created on Mar 3, 2014

@author: orlando.signer@students.unibe.ch
'''
import unittest
import sys, os
sys.path.insert(0, os.path.dirname('../src/MasterPluginGuiCreator.py'))
import MasterPluginGuiCreator as importer
from MasterPluginGuiCreator import ExcelRow
from xml.etree import ElementTree


CONST_EXCEl_FILENAME = "resources/importExcel_20140428.xls"
CONST_EXCEl_FILENAME_SIMPLE = "resources/importExcel_20140428_simple.xls"

CONST_XML_FILENAME = "../../../Gui/GuiIteration4.ui"

class MasterPluginGuiCreatorTest(unittest.TestCase):

    def testCreatePlugin(self):
        importer.createPluginGui(CONST_EXCEl_FILENAME, CONST_XML_FILENAME, 'output.ui')
        
    def testCreatePluginSimple(self):
        importer.createPluginGui(CONST_EXCEl_FILENAME_SIMPLE, CONST_XML_FILENAME, 'output_simple.ui')

    def testImportExcel(self):
        result = importer.importExcel(CONST_EXCEl_FILENAME)
        self.assertNotEqual(None, result, 'result is none')
        self.assertEquals(34, len(result))
        self.assertEquals('Nr.', result[100].name)
        self.assertTrue(result[100].isVariabel)
        self.assertFalse(result[300].isVariabel)
        
    def testImportXml(self):
        tree = ElementTree.parse(CONST_XML_FILENAME)
        result = importer.getXmlWidgets(tree)
        
        self.assertNotEqual(None, result)
        self.assertEqual(55, len(result))
        
    def testSetWidgetInvisible(self):
        widget = ElementTree.Element('widget')
        importer.setWidgetInvisible(widget)
        
        self.assertNotEqual(None, widget.find('./property'))
        self.assertNotEqual(None, widget.find("./property[@name='visible']"))
        self.assertEqual('false', widget.find("./property[@name='visible']/bool").text)
        
    def testSetWidgetText(self):
        widget = ElementTree.Element('widget', name='label_101')
        prop = ElementTree.SubElement(widget, 'property', name='text')
        string = ElementTree.SubElement(prop, 'string')
        string.text = '42'
        element = ExcelRow(101, '1337', False, 'String', [])
        importer.setWidgetText(widget, element)
        
        self.assertEqual('1337', widget.find("./property[@name='text']/string").text)
        self.assertEqual('label_1337', widget.get('name'))
        
    def testSetWidgetTextCombobox(self):
        widget = ElementTree.Element('widget', {'name':'combobox_101', 'class':'QComboBox'})
        comboboxItems = [0,1,2,3,4]
        element = ExcelRow(101, '1337', False, 'combobox', comboboxItems)
        importer.setWidgetText(widget, element)
        
        self.assertIsNone(widget.find("./property[@name='text']/string"))
        self.assertEqual('combobox_1337', widget.get('name'))
        items = widget.findall("./item")
        self.assertEquals(5, len(items))
        for i in range(0,4):
            item = items[i]
            string = item.find("./property/string")
            self.assertEquals(i, string.text)