import pyodbc
import pandas as pd

def _local_db_connect(mdb_path:str=None):
    if mdb_path is None:
        print("ERR - mdb_path is None !")
        return None, None

    print("DB Conn:", mdb_path)
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+mdb_path+';')
    cursor = conn.cursor()

    return conn, cursor

def search_sibling_nodes(word:str=None, mdb_path:str=None):
    # init
    if word is None:
        print("ERR - Word is None !")
        return

    # db connect
    conn, cursor = _local_db_connect(mdb_path)
    if (conn is None) or (cursor is None):
        print("ERR - Plz check mdb_path:", mdb_path)
        return

    # query
    query = """
        SELECT * FROM 
        tblWN_SEIndex 
        WHERE fldWNI_ONTOLOGY = 'KORLEX'  
        AND fldWNI_WORD like '%s';
    """ % word
    print(query.strip())
    rows_df = pd.read_sql(query, conn)
    print(rows_df)

    conn.close()


if "__main__" == __name__:
    mdb_path = "../db/20170726_KorLexDB.mdb"
    search_sibling_nodes(word="먹다", mdb_path=mdb_path)