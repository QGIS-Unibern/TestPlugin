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
        for row in range(sheet.nrows):
            print sheet.row(row)
            
        workbook.release_resources()
        return None