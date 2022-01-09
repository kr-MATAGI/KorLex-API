import pyodbc
import pandas as pd

# set up some constants
MDB_PATH = '../db/20170726_KorLexDB.mdb'

# connect to db
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};DBQ='+MDB+';')
print(MDB_PATH)
cnxn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+MDB_PATH+';')
cursor = cnxn.cursor()

queryArr = []
queryArr.append("SELECT")
queryArr.append("*")
queryArr.append("FROM tblWN_SSINfo")
queryStr = " ".join(queryArr)

rows = pd.read_sql(queryStr, cnxn)

print(len(rows))
print(rows["fldXml"])
cnxn.close()