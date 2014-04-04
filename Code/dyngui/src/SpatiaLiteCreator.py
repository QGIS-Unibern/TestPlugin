'''

@author: stephan.matter@students.unibe.ch
'''
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/pyspatialite-2.6.1')))

import MasterPluginGuiCreator as guiCreator
from pyspatialite import dbapi2 as db

def createSpatiaLiteDatabase(excelPath, projectName):
    '''
    Main Method
    Creates a Spatialite-database with given attribute Names as Excel sheet
    The name of the file will be 'projectName.sqlite'
    '''
    excelElements = guiCreator.importExcel(excelPath)
    attributeNames = extractAttributeNames(excelElements)
    createTables(attributeNames[0], attributeNames[1], projectName)

def extractAttributeNames(excelElements):
    '''
    Gets attribute names and datatypes from the dictionary
    '''
    varNames = []
    statNames = []
    for key, ExcelRow in excelElements.iteritems():
        if ExcelRow.isVariabel == 1:
            varNames.append([ExcelRow.name, ' VARCHAR(50)'])
        else:
            statNames.append([ExcelRow.name, ' VARCHAR(50)'])
    return [statNames, varNames]
        
    
def createTables(statNames, varNames, projectName):
    '''
    Creates a new Spatialite-database with
    - one geometry-layer (polygon) which also stores constant data
    - one geometry-less layer which stores variable data
    '''
    conn = db.connect(projectName+'.sqlite')
    cur = conn.cursor()
    
    sql = "SELECT InitSpatialMetadata()"
    cur.execute(sql)
    sql = "CREATE TABLE '" + projectName + "_const' ("
    sql += "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    for attribute in statNames:
        sql += "'" + attribute[0] + "' " + attribute[1] + ","
    sql = sql[:-1]
    sql += ")"
    cur.execute(sql)
    
    sql = "SELECT AddGeometryColumn('"+projectName+"_const', " 
    sql += "'geometry', 4326, 'POLYGON', 'XY')" 
    cur.execute(sql)
    
    sql = "CREATE TABLE '" + projectName + "_var' ("
    sql += "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    sql += "parent_id INTEGER REFERENCES '" + projectName + "_const',"
    for attribute in varNames:
        sql += "'" + attribute[0] + "' " + attribute[1] + ","
    sql = sql[:-1]
    sql += ")"
    cur.execute(sql)
