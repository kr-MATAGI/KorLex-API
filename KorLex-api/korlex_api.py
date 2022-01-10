import pyodbc
import pandas as pd
from xml.etree import ElementTree as elemTree
import json

## Not Built-in
from korlexDef import *


### METHOD ###
def _local_db_connect(mdb_path:str=None):
    if mdb_path is None:
        print("[_local_db_connect]ERR - mdb_path is None !")
        return None, None

    print("DB Conn:", mdb_path)
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+mdb_path+';')
    cursor = conn.cursor()

    return conn, cursor

def search_synset_info(conn:pyodbc.Connection=None, mdb_path:str=None, soff:str=None, pos:str=None):
    ret_synset_data = SynsetData([], [], [])
    ret_synset_data.word_list = []
    ret_synset_data.parent_list = []
    ret_synset_data.child_list = []

    if (soff is None) or (0 >= len(soff)):
        print("[search_synset_info]ERR - soff is None !")
        return ret_synset_data

    # db connect
    is_inner_db_connect = False
    if conn is None:
        is_inner_db_connect = True
        conn, cursor = _local_db_connect(mdb_path)
        if (conn is None) or (cursor is None):
            print("[search_synset_info]ERR - Plz check mdb_path:", mdb_path)
            return ret_synset_data

    synset_query = ""
    if pos is None:
        synset_query = KORLEX_QUERY.SEARCH_SSINFO.value % soff
    else:
        synset_query = (KORLEX_QUERY.SEARCH_POS_SSINFO.value) % (pos, soff)
    synset_info_df = pd.read_sql(synset_query, conn)

    for idx, ss_info in synset_info_df.iterrows():
        syn_xml = ss_info["fldXml"]
        if 0 >= len(syn_xml):  # xml is available NULL.
            break
        root_tree = elemTree.fromstring(syn_xml)

        # WORD
        word_node_list = root_tree.findall("WORD")
        for word_node in word_node_list:
            word_text = word_node.text
            sense_id = word_node.get("senseid")

            ret_synset_data.word_list.append((word_text, sense_id))

        # Parent / Child
        pointer_node_list = root_tree.findall("POINTER")
        for pt_node in pointer_node_list:
            symbol = pt_node.get("symbol")
            tsoff = pt_node.get("tsoff")
            if "parent" == symbol:
                ret_synset_data.parent_list.append(tsoff)
            elif "child" == symbol:
                ret_synset_data.child_list.append(tsoff)

    if is_inner_db_connect:
        conn.close()

    ret_synset_data.word_list.sort(key=lambda x: x[1])
    return ret_synset_data

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

def search_soff_childern(conn:pyodbc.Connection=None, mdb_path:str=None, soff:str=None):
    ret_child_list = []

    if (soff is None) or (0 >= len(soff)):
        print("[search_soff_childern]ERR - Word is None !")
        return ret_child_list

    # DB
    is_inner_db_connect = False
    if conn is None:
        is_inner_db_connect = True
        conn, cursor = _local_db_connect(mdb_path)
        if (conn is None) or (cursor is None):
            print("[search_soff_childern]ERR - Plz check mdb_path:", mdb_path)
            return ret_child_list

    query = KORLEX_QUERY.SEARCH_SSINFO.value % soff
    synset_info_df = pd.read_sql_query(query, conn)

    for idx, ss_info in synset_info_df.iterrows():
        syn_xml = ss_info["fldXml"]
        if 0 >= len(syn_xml):  # xml is available NULL.
            break
        root_tree = elemTree.fromstring(syn_xml)

        # Parent / Child
        pointer_node_list = root_tree.findall("POINTER")
        for pt_node in pointer_node_list:
            symbol = pt_node.get("symbol")
            tsoff = pt_node.get("tsoff")
            if "child" == symbol:
                ret_child_list.append(tsoff)

    if is_inner_db_connect:
        conn.close()

    return ret_child_list

def make_korlex_tree_resource(word:str=None, mdb_path:str=None):
    ret_json_rsrc_list = []

    if word is None:
        print("[make_korlex_word_tree]ERR - Word is None !")
        return ret_json_rsrc_list

    # DB
    conn, cursor = _local_db_connect(mdb_path=mdb_path)
    if (conn is None) or (cursor is None):
        print("[make_korlex_word_tree]ERR - Plz check mdb_path:", mdb_path)
        return ret_json_rsrc_list

    # search target info (search synset)
    search_target_info = search_sibling_nodes(conn=conn, word=word, mdb_path=mdb_path)

    # Make Tree (format. json)
    for st_info in search_target_info:
        search_target_synset = search_synset_info(conn=conn, soff=st_info.soff, pos=st_info.pos)

        parent_json_data_list = []
        origin_json = KorLexJson(synset=[])
        origin_json.synset = [(st_info.word, st_info.senseId)]
        origin_json.soff = st_info.soff
        for target_parent in search_target_synset.parent_list:
            parent_json_data = []
            parent_json_data.append(origin_json)

            target_soff = target_parent
            target_pos = st_info.pos
            while None != target_soff:
                # Search Synset
                sysnset_data = search_synset_info(conn=conn, soff=target_soff, pos=target_pos)
                korlex_json = KorLexJson(synset=[])
                korlex_json.synset = sysnset_data.word_list
                korlex_json.soff = target_soff
                parent_json_data.append(korlex_json)

                # Search relation index
                target_soff = serach_relation_index_info(conn=conn, soff=target_soff)
            parent_json_data_list.append(parent_json_data)
        ret_json_rsrc_list.append(parent_json_data_list)

    # DB close
    conn.close()

    return ret_json_rsrc_list


def make_korlex_result_json(json_rsrc_list:list):
    json_dict = {
        "ontology": "korlex",
        "search_word": "",
        "search_senseid": "",
        "results": []
    }

    # Make Dict
    for json_rsrc in json_rsrc_list:
        if "" == json_dict["search_word"]:
            json_dict["search_word"] = json_rsrc[0].synset[0][0]
            json_dict["search_senseid"] = str(json_rsrc[0].synset[0][1])

        json_rsrc.reverse()
        for rsrc_item in json_rsrc:
            item_dict = {
                "word_sets": [],
                "soff": rsrc_item.soff
            }

            for word in rsrc_item.synset:
                word_dict = {
                    "word": word[0],
                    "senseid": word[1]
                }
                item_dict["word_sets"].append(word_dict)
            json_dict["results"].append(item_dict)

    ret_json = json.dumps(json_dict, ensure_ascii=False).encode("utf8")
    print(ret_json.decode())

### TEST ###
if "__main__" == __name__:
    mdb_path = "../db/20170726_KorLexDB.mdb"

    # json_rsc_list = make_korlex_tree_resource(word="사과", mdb_path=mdb_path)
    # print(json_rsc_list)

    test_rsrc = [[KorLexJson(synset=[('사과', 2)], soff='07267116'), KorLexJson(synset=[('실과', '1'), ('과일', '1'), ('과실', '2')], soff='07234431'), KorLexJson(synset=[('청과물', '1')], soff='07234211'), KorLexJson(synset=[('고형 식품', '1')], soff='07089248'), KorLexJson(synset=[('고체', '2')], soff='14193490'), KorLexJson(synset=[('성분', '1'), ('물질', '1')], soff='00017572'), KorLexJson(synset=[('실체', '1'), ('개체', '1')], soff='00001740')], [KorLexJson(synset=[('사과', 2)], soff='07267116'), KorLexJson(synset=[('이과', '2')], soff='12386033'), KorLexJson(synset=[('열매', '1'), ('과실', '3')], soff='12382403'), KorLexJson(synset=[('생식기', '1'), ('생식기관', '1')], soff='10930823'), KorLexJson(synset=[('식물기관', '1')], soff='12336912'), KorLexJson(synset=[('식물구조', '1')], soff='12336213'), KorLexJson(synset=[('자연물', '1')], soff='00017087'), KorLexJson(synset=[('물체', '1'), ('물건', '1')], soff='00016236'), KorLexJson(synset=[('실체', '1'), ('개체', '1')], soff='00001740')]]
    make_korlex_result_json(test_rsrc)

