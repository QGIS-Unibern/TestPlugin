'''

@author: stephan.matter@students.unibe.ch
'''
import unittest
import sys, os
sys.path.insert(0, os.path.dirname('../src/SpatiaLiteExporter.py'))
import SpatiaLiteExporter as exporter
from pyspatialite import dbapi2 as db

CONST_SQLITE_FILENAME = "resources/projectName1660.sqlite"
columnNamesConst = ['id', 'Abwasserkanal', 'Schmutzwasser', 'Mischwasser', 'Regenwasser', 
               'Frischwasser', 'Leitung Erdgas', 'Leitung Fernwaerme', 'Leitung Fernseh', 
               'Leitung Telefon', 'Leitung Glasfaser', 'Leitung Strom', 'Fotos', 'PDF', 
               'Word', 'Excel', 'Strasse', 'Abschnitt', 'Verkehrsfuehrung', 'Material Deckschicht', 
               'Dicke Deckschicht', 'Dicke Binderschicht', 'Dicke Asphalt-Tragschicht', 
               'Dicke Schotter-tragschicht', 'Dicke Frostschutzschicht', 'geometry']

columnNamesVar = ['id', 'parent_id', 'Hausnummer kleinste', 'Hausnummer groesste', 
                 'Breite Fahrbereich', 'Breite Weg links', 'Breite Weg rechts', 'Fotos', 
                 'PDF-Dateien', 'Word-Dateien', 'Excel-Dateien', 'Export', 'Nr.', 'von', 
                 'Event', 'Datum JJJJMMTT', 'Art der Arbeit', 'Firma', 'Person', 'Vermerk']

class SpatiaLiteExporterTest(unittest.TestCase):
    '''
    PDF-export geht noch nicht
    def testPdfExport(self):
        curDir = os.path.dirname(os.path.realpath(__file__))
        exporter.exportPDF(CONST_SQLITE_FILENAME, 
                           "projectName1660", 2, [],curDir + "test.pdf")
    '''
    
    def testGetConstAttributes(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getConstAttributes(cur, "projectName1660")
        self.assertEqual(columnNamesConst, data)
        conn.close()
        
    def testGetVarAttributes(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getVarAttributes(cur, "projectName1660")
        self.assertEqual(columnNamesVar, data)
        conn.close()
        
    def testGetConstData(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getConstData(cur, "projectName1660", 2)
        self.assertEqual("vielleciht",data[0][10])
        self.assertEqual("Guguselistrasse",data[0][16])
        conn.close()
        
    def testGetVarData(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getVarData(cur, "projectName1660", 2)
        self.assertNotEqual(None, data)
        conn.close()