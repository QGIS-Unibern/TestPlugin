'''

@author: orlando.signer@students.unibe.ch
'''

import xlrd

class ExcelImport(object):
    '''
    classdocs
    '''
    
    def __init__(self, ):
        '''
        Constructor
        '''
        
    def importFile(self, filename):
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        guiElements = []
        for i in range(sheet.nrows):
            if i == 0: 
                continue # first line contains titles
            row = sheet.row(i)
            guiElements.append(GuiElement(row[1], row[4]))
            
        workbook.release_resources()
        return guiElements
    
class GuiElement(object):
    def __init__(self, varId, name):
        if varId is None or name is None:
            raise ValueError("varId (%varId) or name (%name) is none!", varId, name)
        self.varId = varId
        self.name = name
        
    def __str__(self, *args, **kwargs):
        return str(self.__dict__)
        
    def __cmp__(self, other):
        return self.varId == other.varId and self.name == other.name
    
    def __hash__(self, *args, **kwargs):
        return hash(self.varId, self.name)
