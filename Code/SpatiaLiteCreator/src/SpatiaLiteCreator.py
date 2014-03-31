'''

@author: stephan.matter@students.unibe.ch
'''
import MasterPluginGuiCreator as guiCreator
from pyspatialite import dbapi2 as db

def createSpatiaLiteDatabase(excelPath, projectName):
    
    excelElements = guiCreator.importExcel(excelPath)
    attributeNames = extractAttributeNames(excelElements)
    createTables(statNames, varNames)

def extractAttributeNames(excelElements):
    '''
    Gets attribute names and datatypes from the dictionary
    '''
    for key, value in excelElements.iteritems():
        value = 0
    
def createTables(statNames, varNames, projectName):
    '''
    Creates a new Spatialite-database with
    - one geometry-layer (polygon) which also stores constant data
    - one geometry-less layer which stores variable data
    '''
    conn = db.connect(name+'.sqlite')
    cur = conn.cursor()
    sql = 'SELECT InitSpatialMetadata()'
    cur.execute(sql)
    sql = 'CREATE TABLE ' + projectName + 'const ('
    sql += 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    for attribute in statNames:
        sql += attribute + ' VARCHAR(50), '
    cur.execute(sql)
    
    sql = 'CREATE TABLE ' + projectName + 'var ('
    sql += 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    sql += 'parent_id INTEGER REFERENCES ' + projectName + 'const,'
    for attribute in varNames:
        sql += attribute + ' VARCHAR(50), '
    cur.execute(sql)