'''
Created on Mar 3, 2014

@author: orlando.signer@students.unibe.ch
'''
import unittest
import ExcelImport
from ExcelImport import GuiElement

CONST_EXCEl_FILENAME = "resources/20140301_Bern_Excel-Input-Tabelle_Attributnamen.xls"
CONST_XML_FILENAME = "../../../Gui/GUIersterVersuchWoche3.ui"

class ExcelImportTest(unittest.TestCase):

    
    def testImportExcel(self):
        importer = ExcelImport.ExcelImport()
        result = importer.importExcel(CONST_EXCEl_FILENAME)
        self.assertNotEqual(None, result, 'result is none')
        self.assertEquals(42, len(result))
        self.assertEquals(GuiElement(100, 'Nr.'), result[0])
        
    def testImportXml(self):
        importer = ExcelImport.ExcelImport()
        importer.importXML(CONST_XML_FILENAME)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()