'''
    Ref: ../document/query.md
'''

import pyodbc
import pandas as pd

# set up some constants
MDB_PATH = '../db/20170726_KorLexDB.mdb'

# Connect to DB
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+MDB_PATH+';')
cursor = conn.cursor()

## 1. [tblWN_ELEMENTS]
test_query_1 = "SELECT * FROM [tblWN_ELEMENTS] WHERE [fldWNE_ONTOLOGY] = 'KORLEX' AND [fldWNE_POS] = 'n' AND [fldWNE_SEARCH] like '데이터'"
rows = pd.read_sql(test_query_1, conn)
print(rows)

conn.close()