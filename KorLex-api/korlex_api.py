import pyodbc
import pandas as pd
from xml.etree import ElementTree as elemTree

## Not Built-in
from korlexDef import *


def _local_db_connect(mdb_path:str=None):
    if mdb_path is None:
        print("[_local_db_connect]ERR - mdb_path is None !")
        return None, None

    print("DB Conn:", mdb_path)
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+mdb_path+';')
    cursor = conn.cursor()

    return conn, cursor

def search_synset_info(conn:pyodbc.Connection=None, mdb_path:str=None, soff:str=None, pos:str=None):
    ret_synset_list = []

    if (soff is None) or (0 >= len(soff)):
        print("[search_synset_info]ERR - soff is None !")
        return ret_synset_list

    # db connect
    is_inner_db_connect = False
    if conn is None:
        is_inner_db_connect = True
        conn, cursor = _local_db_connect(mdb_path)
        if (conn is None) or (cursor is None):
            print("ERR - Plz check mdb_path:", mdb_path)
            return ret_synset_list

    synset_query = (KORLEX_QUERY.SEARCH_SSINFO.value) % (pos, soff)
    synset_info_df = pd.read_sql(synset_query, conn)

    for idx, ss_info in synset_info_df.iterrows():
        syn_xml = ss_info["fldXml"]
        print(syn_xml)
        if 0 >= len(syn_xml):  # xml is available NULL.
            break

        root_tree = elemTree.fromstring(syn_xml)
        word_node_list = root_tree.findall("WORD")
        for word_node in word_node_list:
            word_text = word_node.text
            sense_id = word_node.get("senseid")

            ret_synset_list.append((word_text, sense_id))

    if is_inner_db_connect:
        conn.close()

    ret_synset_list.sort(key=lambda x: x[1])
    return ret_synset_list

def search_sibling_nodes(conn:pyodbc.Connection=None, mdb_path:str=None, word:str=None):
    # init
    siblingNodeList = []

    if word is None:
        print("[search_sibling_nodes]ERR - Word is None !")
        return siblingNodeList

    # db connect
    is_inner_db_connect = False
    if conn is None:
        is_inner_db_connect = True
        conn, cursor = _local_db_connect(mdb_path)
        if (conn is None) or (cursor is None):
            print("[search_sibling_nodes]ERR - Plz check mdb_path:", mdb_path)
            return siblingNodeList

    # query
    query = KORLEX_QUERY.SEARCH_SIBLING_NODE.value % word
    rows_df = pd.read_sql(query, conn)

    if is_inner_db_connect:
        conn.close()

    # retrun
    for idx, row in rows_df.iterrows():
        siblingNode = SiblingNode()
        siblingNode.ontology = row["fldWNI_ONTOLOGY"]
        siblingNode.pos = row["fldWNI_POS"]
        siblingNode.soff = row["fldWNI_SOFF"]
        siblingNode.word = row["fldWNI_WORD"]
        siblingNode.senseId = row["fldWNI_SENSEID"]

        siblingNodeList.append(siblingNode)

    return siblingNodeList

def serach_relation_index_info(conn:pyodbc.Connection=None, mdb_path:str=None, soff:str=None):
    ret_element = None

    if (soff is None) or (0 >= len(soff)):
        print("[serach_relation_index_info]ERR - Word is None !")
        return ret_element

    # DB
    is_inner_db_connect = False
    if conn is None:
        is_inner_db_connect = True
        conn, cursor = _local_db_connect(mdb_path)
        if (conn is None) or (cursor is None):
            print("[serach_relation_index_info]ERR - Plz check mdb_path:", mdb_path)
            return ret_element

    # Search realtion index
    query = KORLEX_QUERY.SEARCH_REL_IDX.value % soff
    rel_idx_df = pd.read_sql(query, conn)

    for idx, rel_info in rel_idx_df.iterrows():
        if "child" == rel_info["fldWNIR_RELATION"]:
            ret_element = rel_info["fldWNIR_ELEMENT"]
            break

    if is_inner_db_connect:
        conn.close()

    return ret_element

def make_korlex_word_tree(word:str=None, mdb_path:str=None):
    ret_tree_json_list = []

    if word is None:
        print("[make_korlex_word_tree]ERR - Word is None !")
        return ret_tree_json_list

    # DB
    conn, cursor = _local_db_connect(mdb_path=mdb_path)
    if (conn is None) or (cursor is None):
        print("[make_korlex_word_tree]ERR - Plz check mdb_path:", mdb_path)
        return ret_tree_json_list

    # search target info (search synset)
    search_target_info = search_sibling_nodes(conn=conn, word=word, mdb_path=mdb_path)

    # Make Tree (format. json)
    for info in search_target_info:
        korlex_tree = KorLexTreeJson()
        korlex_tree.element_info = info

        target_soff = info.soff
        target_pos = info.pos
        while None != target_soff:
            # Search Synset
            synset_list = search_synset_info(conn=conn, soff=target_soff, pos=target_pos)
            print(synset_list)

            # Search relation index
            target_soff = serach_relation_index_info(conn=conn, soff=target_soff)
            print(target_soff)

    conn.close()

    return ret_tree_json_list

if "__main__" == __name__:
    mdb_path = "../db/20170726_KorLexDB.mdb"

    a = make_korlex_word_tree(word="사과", mdb_path=mdb_path)
    #search_synset_info(soff="06089217", mdb_path=mdb_path)