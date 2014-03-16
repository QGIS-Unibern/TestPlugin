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
        with open(CONST_XML_FILENAME, 'r') as content_file:
            content = content_file.read()
        tree = ElementTree.XML(content)
        importer = ExcelImport.ExcelImport()
        result = importer.getXmlWidgets(tree)
        
        self.assertNotEqual(None, result)
        self.assertEqual(86, len(result))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()