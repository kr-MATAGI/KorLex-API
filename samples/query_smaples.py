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
query_1 = "SELECT * FROM [tblWN_ELEMENTS] WHERE [fldWNE_ONTOLOGY] = 'KORLEX' AND [fldWNE_POS] = 'n' AND [fldWNE_SEARCH] like '사과'"
rows = pd.read_sql(query_1, conn)
print("QUERY_1:", query_1)
#print(rows.values)

## 2. tblWN_SEIndex
query_2_1 = "SELECT * FROM [tblWN_SEIndex] WHERE [fldWNI_ONTOLOGY] = 'KORLEX' AND [fldWNI_POS] = 'n' AND fldWNI_WORD like '사과'"
rows = pd.read_sql(query_2_1, conn)
print("QUERY_2_1:", query_2_1)
#print(rows)

query_2_2 = "SELECT * FROM [tblWN_SEIndex] WHERE [fldWNI_ONTOLOGY] = 'KORLEX' AND [fldWNI_POS] = 'n' AND fldWNI_SOFF LIKE '06224165'"
rows = pd.read_sql(query_2_2, conn)
print("QUERY_2_2:", query_2_2)
#print(rows, "\n")

## 3. tblWN_SSInfo
query_3 = "SELECT * FROM [tblWN_SSInfo] WHERE [fldOntology] = 'KORLEX' AND [fldPos] = 'n' AND fldSoff like '06224165'"
rows = pd.read_sql(query_3, conn)
print("QUERY_3:", query_3)

# for i, r in rows.iterrows():
#     print(r)

xml_str = rows["fldXml"][0]
# print("XML:", xml_str, "\n")

## 4. tblWN_RelIndex
query_4_1 = "SELECT * FROM [tblWN_RelIndex] WHERE [fldWNIR_ONTOLOGY] = 'KORLEX' AND [fldWNIR_POS] = 'n' AND fldWNIR_ELEMENT LIKE '06224165'"
rows = pd.read_sql(query_4_1, conn)
print("QUERY_4_1:", query_4_1)

query_4_2 = "SELECT * FROM [tblWN_RelIndex] WHERE [fldWNIR_ONTOLOGY] = 'KORLEX' AND [fldWNIR_TRGPOS] = 'n' AND fldWNIR_TRGELEMENT LIKE '06224165'"
rows = pd.read_sql(query_4_2, conn)
print("QUERY_4_2:", query_4_2)
for i, r in rows.iterrows():
    print(r)
exit()

conn.close()