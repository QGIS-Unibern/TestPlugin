'''
Created on Mar 3, 2014

@author: orlando.signer@students.unibe.ch
'''
import unittest
import ExcelImport
from xml.etree import ElementTree

CONST_EXCEl_FILENAME = "resources/20140301_Bern_Excel-Input-Tabelle_Attributnamen.xls"
CONST_XML_FILENAME = "../../../Gui/GUIersterVersuchWoche3.ui"

class ExcelImportTest(unittest.TestCase):
    
    def testCreatePlugin(self):
        importer = ExcelImport.ExcelImport()
        importer.createPluginGui(CONST_EXCEl_FILENAME, CONST_XML_FILENAME, 'output.ui')

    
    def testImportExcel(self):
        importer = ExcelImport.ExcelImport()
        result = importer.importExcel(CONST_EXCEl_FILENAME)
        self.assertNotEqual(None, result, 'result is none')
        self.assertEquals(42, len(result))
        self.assertEquals('Nr.', result[100])
        
    def testImportXml(self):
        tree = ElementTree.parse(CONST_XML_FILENAME)
        importer = ExcelImport.ExcelImport()
        result = importer.getXmlWidgets(tree)
        
        self.assertNotEqual(None, result)
        self.assertEqual(86, len(result))
        
    def testSetWidgetInvisible(self):
        widget = ElementTree.Element('widget')
        importer = ExcelImport.ExcelImport()
        importer.setWidgetInvisible(widget)
        
        self.assertNotEqual(None, widget.find('./property'))
        self.assertNotEqual(None, widget.find("./property[@name='visible']"))
        self.assertEqual('false', widget.find("./property[@name='visible']/bool").text)
        
    def testSetWidgetText(self):
        widget = ElementTree.Element('widget')
        prop = ElementTree.SubElement(widget, 'property', name='text')
        string = ElementTree.SubElement(prop, 'string')
        string.text = '42'
        
        importer = ExcelImport.ExcelImport()
        importer.setWidgetText(widget, '1337')
        
        self.assertEqual('1337', widget.find("./property[@name='text']/string").text)
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()