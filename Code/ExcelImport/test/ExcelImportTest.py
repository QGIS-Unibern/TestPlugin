'''
Created on Mar 3, 2014

@author: orlando.signer@students.unibe.ch
'''
import unittest
import ExcelImport
from ExcelImport import GuiElement

CONST_FILENAME = "resources/20140301_Bern_Excel-Input-Tabelle_Attributnamen.xls"

class ExcelImportTest(unittest.TestCase):

    
    def testImport(self):
        importer = ExcelImport.ExcelImport()
        result = importer.importFile(CONST_FILENAME)
        self.assertNotEqual(None, result, 'result is none')
        self.assertEquals(42, len(result))
        self.assertEquals(GuiElement(100, 'Nr.'), result[0])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()