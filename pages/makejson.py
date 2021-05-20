import xlrd
from collections import OrderedDict
import json


wb = xlrd.open_workbook('magoosh1000.xlsx')
sheet = wb.sheet_by_index(0)

data_list = []

for i in range(1, 1067):

    now = OrderedDict()	

    now['word'] = sheet.cell_value(i, 0).encode('utf-8').strip()    
    now['pos'] = sheet.cell_value(i, 2).encode('utf-8').strip()    
    now['difinition'] = sheet.cell_value(i, 1).encode('utf-8').strip()    
    now['example'] = sheet.cell_value(i, 3).encode('utf-8').strip()    
    # now['pos'] = str(sheet.cell_value(i, 2))    
    # now['definition'] = str(sheet.cell_value(i, 1))    
    # now['example'] = str(sheet.cell_value(i, 3))
    data_list.append(now) 

    # print(now)   

with open("magoosh1000.json", "w") as writeJsonfile:
      json.dump(data_list, writeJsonfile, indent=4,default=str)
