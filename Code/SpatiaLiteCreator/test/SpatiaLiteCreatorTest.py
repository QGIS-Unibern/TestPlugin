'''

@author: stephan.matter@students.unibe.ch
'''
import unittest
import sys, os
sys.path.insert(0, os.path.dirname('../src/SpatiaLiteCreator.py'))
import SpatiaLiteCreator as creator

try: 
    os.remove('test_simple.sqlite')
    os.remove('test_umlaute.sqlite')
    os.remove('test.sqlite')
except OSError:
    pass

CONST_EXCEl_FILENAME = "resources/importExcel_20140428.xls"
CONST_EXCEl_FILENAME_SIMPLE = "resources/importExcel_20140428_simple.xls"
CONST_EXCEl_FILENAME_UMLAUTE = "resources/importExcel_20140428_umlaute.xls"
HERE = os.path.dirname(os.path.realpath(__file__))

class SpatiaLiteCreatorTest(unittest.TestCase):
    
    def testSpatiaLiteCreatorSimple(self):
        creator.createSpatiaLiteDatabase(CONST_EXCEl_FILENAME_SIMPLE, 'test_simple', HERE)
        
    def testSpatiaLiteCreatorUmlaute(self):
        creator.createSpatiaLiteDatabase(CONST_EXCEl_FILENAME_UMLAUTE, 'test_umlaute', HERE)    
''' 
    def testSpatiaLiteCreator(self):
        creator.createSpatiaLiteDatabase(CONST_EXCEl_FILENAME, 'test')
'''