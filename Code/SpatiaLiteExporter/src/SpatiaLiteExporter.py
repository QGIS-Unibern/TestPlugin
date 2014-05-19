'''

@author:stephan.matter@students.unibe.ch
'''
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/reportlab-3.0/src')))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/pyspatialite-2.6.1')))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/svgfig')))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../libs/svglib-0.6.3/src')))

from pyspatialite import dbapi2 as db
from svgfig import *
import svgfig as svgfig
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.renderPDF import GraphicsFlowable
from reportlab.pdfgen import canvas

''' 
Exports all data of geometric objects
---
Input:
spatiaLitePath: Path to the SpatiaLite file
parentTable: Name of the table where the selected polygon is
objectId: Ids of the selected polygons (table primary key)
attributeNames: Names of the attributes to export
    It has to be a list of two lists like [constAttributes, varAttributes]
    Where constAttribtues = {attribute1, attribute2, ...} of the constant table
    and the same for varAttributes.
outputPath: Path where the output pdf will be located
---
This function will search for all geometric objects in childTables that intersect with the
selected object in the parentTable and output all their data as PDF
'''
def exportPDF(spatiaLitePath, table, objectIds, attributeNames, outputPath):
    tabledata = []
    for index in objectIds:
        tabledata.append(extractData(spatiaLitePath, table, index, attributeNames))
    doc = Document(outputPath, table)
    style = ParagraphStyle(name='Normal',
                           fontName='Helvetica-Bold',
                           fontSize=12,)
    doc.append([Paragraph(table,style)])
    for index, value in enumerate(objectIds):
        doc.append(formatData(tabledata[index], doc))
    doc.build()
  
'''
Formats the tables for reportlab
'''
def formatData(tabledata, doc):
    elements = []
    constData = []
    #elements.append(GraphicsFlowable(tabledata[4]))
    elements.append(Spacer(width=1, height=30))
    style = ParagraphStyle(name='Normal',
                           fontName='Helvetica-Bold',
                           fontSize=9,)
    elements.append(Paragraph("Constant Data",style))
    
    med = int(round(float(len(tabledata[1]))/2))
    for index, item in enumerate(tabledata[1]):
        if index < med:
            constData.append([tabledata[0][index]+":", item])
        else:
            constData[index-med].append(tabledata[0][index]+":")
            constData[index-med].append(item)
    const = Table(constData,4*[doc.width/4])
    const.hAlign = "LEFT"
    const.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('LINEABOVE', (0,0), (3,0), 2, colors.black),
                               ('LEFTPADDING', (1,0), (1,-1), 10),
                               ('LEFTPADDING', (3,0), (3,-1), 10)]))
    elements.append(const)
    if tabledata[3]:
        elements.append(Paragraph("Event Data",style))
    for datalist in tabledata[3]:
        varData = []
        for i, item in enumerate(datalist):
            varData.append([tabledata[2][i], item])
        var = Table(varData,2*[doc.width/2])
        var.hAlign = "LEFT"
        var.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                 ('LINEABOVE', (0,0), (3,0), 2, colors.black)]))
        elements.append(var)
    return elements
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
def extractData(spatiaLitePath, tableName, id, attributes):
    try:
        conn = db.connect(spatiaLitePath)
        cur = conn.cursor()
        constAttributes = getConstAttributes(cur, tableName)
        varAttributes = getVarAttributes(cur, tableName)
        constData = getConstData(cur, tableName, id)
        varData = getVarData(cur, tableName, id)
        image = getGeometryImage(cur, tableName, id)
        
        #Filtering stuff
        if attributes:
            varAttr_ = []
            constAttr_ = []
            constData_ = []
            varData_ = []
            for index, value in enumerate(constAttributes):
                if value in attributes[0]:
                    constAttr_.append(constAttributes[index])
                    constData_.append(constData[index])
        
            for index, value in enumerate(varAttributes):
                if value in attributes[1]:
                    varAttr_.append(varAttributes[index])
                    for i,v in enumerate(varData):
                        if len(varData_) <= i:
                            varData_.append([varData[i][index]])
                        else:
                            varData_[i].append(varData[i][index])
            
            return[constAttr_, constData_, varAttr_, varData_, image]
        
    except db.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit()
        
    finally:
        if conn:
            conn.close()
    return [constAttributes, constData, varAttributes, varData, image]            
                     
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
    t = "x*x, y*y"
    fig = Fig(Path(data[0][0], fill="blue", local="true"), trans=t).SVG()
    svgfig._canvas_defaults["width"] = "100px"
    svgfig._canvas_defaults["height"] = "100px"
    svgfig._canvas_defaults["viewBox"] = "0 0 100 100"
    fig.save(here + "tmp.svg")
    svg = svg2rlg(here + "tmp.svg")
    os.remove(here + "tmp.svg")
    return svg

'''
Helper class for building a document
'''
class Document:
    def __init__(self, outputPath, table):
        self.doc = SimpleDocTemplate(outputPath, pagesize=letter)
        self.width = self.doc.width
        self.elements = []
        self.name = table
        
    def append(self, datalist):
        for item in datalist:
            self.elements.append(item)
        
    def build(self):
        if self.elements != []:
            self.doc.build(self.elements, canvasmaker=NumberedCanvas)
            
'''
Helper class needed for page numbers (I love reportlab)
'''
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(115*mm, 15*mm,
                             "Page %d of %d" % (self._pageNumber, page_count))
