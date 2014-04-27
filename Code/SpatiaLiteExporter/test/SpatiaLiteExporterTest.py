'''

@author: stephan.matter@students.unibe.ch
'''
import unittest
import sys, os
sys.path.insert(0, os.path.dirname('../src/SpatiaLiteExporter.py'))
import SpatiaLiteExporter as exporter
from pyspatialite import dbapi2 as db

CONST_SQLITE_FILENAME = "resources/test.sqlite"
columnNamesConst = ['id', 'Abwasserkanal', 'Schmutzwasser', 'Mischwasser', 
                    'Regenwasser', 'Frischwasser', 'Leitung Erdgas', 'Leitung Fernwaerme', 
                    'Leitung Fernseh', 'Leitung Telefon', 'Leitung Glasfaser', 'Leitung Strom', 
                    'Strasse', 'Abschnitt', 'Hausnummer kleinste', 'Hausnummer groesste', 
                    'Breite Fahrbereich', 'Breite Weg links', 'Breite Weg rechts', 
                    'Verkehrsfuehrung', 'Material Deckschicht', 'Dicke Deckschicht', 
                    'Dicke Binderschicht', 'Dicke Asphalt-Tragschicht', 
                    'Dicke Schotter-tragschicht', 'Dicke Frostschutzschicht']

columnNamesVar = ['id', 'parent_id', 'Fotos', 'Nr.', 'von', 'Event', 'Datum JJJJMMTT', 
                  'Art der Arbeit', 'Firma', 'Person', 'Vermerk']

class SpatiaLiteExporterTest(unittest.TestCase):
    
    def testPdfExport(self):
        curDir = os.path.dirname(os.path.realpath(__file__))
        exporter.exportPDF(CONST_SQLITE_FILENAME, 
                           "newProject", [2,1], [],curDir + "test.pdf")
    
    def testGetConstAttributes(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getConstAttributes(cur, "newProject")
        self.assertEqual(columnNamesConst, data)
        conn.close()
        
    def testGetVarAttributes(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getVarAttributes(cur, "newProject")
        self.assertEqual(columnNamesVar, data)
        conn.close()
        
    def testGetConstData(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getConstData(cur, "newProject", 2)
        self.assertEqual("Bernstrasse",data[12])
        conn.close()
        
    def testGetVarData(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getVarData(cur, "newProject", 2)
        self.assertNotEqual(None, data)
        conn.close()
        
    def testGetGeometryImage(self):
        conn = db.connect(CONST_SQLITE_FILENAME)
        cur = conn.cursor()
        data = exporter.getGeometryImage(cur, "newProject", 2)
        self.assertNotEqual(None, data)
        conn.close()