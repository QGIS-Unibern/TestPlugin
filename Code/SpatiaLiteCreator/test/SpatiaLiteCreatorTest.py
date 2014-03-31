'''

@author: stephan.matter@students.unibe.ch
'''
import unittest
import sys, os
sys.path.insert(0, os.path.dirname('../src/SpatiaLiteCreator.py'))
import SpatiaLiteCreator as creator

try: 
    os.remove('test_simple.sqlite')
    os.remove('test.sqlite')
except OSError:
    pass

CONST_EXCEl_FILENAME = "resources/20140301_Bern_Excel-Input-Tabelle_Attributnamen.xls"
CONST_EXCEl_FILENAME_SIMPLE = "resources/20140301_Bern_Excel-Input-Tabelle_Attributnamen_simple.xls"

class SpatiaLiteCreatorTest(unittest.TestCase):
    
    def testSpatiaLiteCreatorSimple(self):
        creator.createSpatiaLiteDatabase(CONST_EXCEl_FILENAME_SIMPLE, 'test_simple')
''' 
    def testSpatiaLiteCreator(self):
        creator.createSpatiaLiteDatabase(CONST_EXCEl_FILENAME, 'test')
'''