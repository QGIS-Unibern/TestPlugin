'''

@author:stephan.matter@students.unibe.ch
'''
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/svglib-0.6.3/src')))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/reportlab-3.0/src')))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/pyspatialite-2.6.1')))

from pyspatialite import dbapi2 as db
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image

''' 
Exports all data of geometric objects
---
Input:
spatiaLitePath: Path to the SpatiaLite file
parentTable: Name of the table where the selected polygon is
objectId: Id of the selected polygon (table primary key)
childTables: list of names of all tables where you want to export the data
outputPath: Path where the output pdf will be located
---
This function will search for all geometric objects in childTables that intersect with the
selected object in the parentTable and output all their data as PDF
'''
def exportPDF(spatiaLitePath, parentTable, objectIds, childTables, outputPath):
    parentData = []
    childData = []
    parentData = extractData(spatiaLitePath, parentTable, objectId[0])
    '''
    for table in childTables:
        childData.append(extractChildData(spatiaLitePath, parentTable, objectId, table))
    '''
    formattedData = formatData(parentData, childData)
    printPdf(outputPath, formattedData)
  
'''
Formats the tables for reportlab
'''
def formatData(parentData, childData):
    elements = []
    constData = []
    for index, item in enumerate(parentData[1]):
        if item != None:
            constData.append([parentData[0][index], item])
    const = Table(constData)
    const.hAlign = "LEFT"
    elements.append(const)
    
    for list in parentData[3]:
        varData = []
        for i, item in enumerate(list):
            if item != None:
                varData.append([parentData[2][i], item])
        var = Table(varData)
        var.hAlign = "LEFT"
        elements.append(var)
    return elements
        
def printPdf(outputPath, data):
    doc = SimpleDocTemplate(outputPath, pagesize=letter)
    doc.build(data)
    
    
'''
Returns an array of list of strings containing all data of object 'id' in table 'tableName'
Output: 
[constAttributes, constData, varAttributes, varData, image]
where: 
constAttributes = {attribute1, attribute2, ...} (list of Strings)
varAttributes = dito
constData = [DataOfAttribute1, DataOfAttribute2, ...] (list of list of Strings)
varData = dito
image = svg representation of the selected geometry
'''
def extractData(spatiaLitePath, tableName, id):
    try:
        conn = db.connect(spatiaLitePath)
        cur = conn.cursor()
        constAttributes = getConstAttributes(cur, tableName)
        varAttributes = getVarAttributes(cur, tableName)
        constData = getConstData(cur, tableName, id)
        varData = getVarData(cur, tableName, id)
        image = getGeometryImage(cur, tableName, id)
    except db.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit()
        
    finally:
        if conn:
            conn.close()
    return [constAttributes, constData, varAttributes, varData, image]
               
'''
Sollte alle IDs von objekten auf einer child-Table finden, die das selektierte objekt schneiden
'''
def extractChildData(spatiaLitePath, parentTable, id, table):
    try:
        conn = db.connect(spatiaLitePath)
        cur = conn.cursor()
        sqlgeom1 = "SELECT geometry FROM '"+parentTable+"' WHERE id="+`id`
        sqlselect = "SELECT id FROM '"+table+"' WHERE TOUCHES(("+sqlgeom1+"),geometry)"
        cur.execute(sqlselect)
        data = cur.fetchall()
    except db.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit()
        
    finally:
        if conn:
            conn.close()
            
    return extractData(spatiaLitePath, table, id)
                
                     
def getConstAttributes(cursor, tableName):
    sql = "SELECT * from '" + tableName + "'"
    cursor.execute(sql)
    names = list(map(lambda x: x[0], cursor.description))
    del names[-1] # Remove geometry
    return names

def getVarAttributes(cursor, tableName):
    sql = "SELECT * from '" + tableName + "_var'"
    cursor.execute(sql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def getConstData(cursor, tableName, id):
    sql = "SELECT * FROM '" + tableName + "' WHERE id=" +`id`
    cursor.execute(sql)
    data = cursor.fetchall()
    dataList = []
    for row in data:
        for item in row:
            dataList.append(item)
    del dataList[-1] # Remove geometry
    return dataList

def getVarData(cursor, tableName, id):
    sql = "SELECT * FROM '" + tableName + "_var' WHERE parent_id=" + `id`
    cursor.execute(sql)
    data = cursor.fetchall()
    dataList = []
    for row in data:
        dataList.append([item for item in row])
    return dataList

def getGeometryImage(cursor, tableName, id):
    sql = "SELECT AsSvg(geometry) FROM '" + tableName + "' WHERE id =" + `id`
    cursor.execute(sql)
    data = cursor.fetchall()
    return data[0]
