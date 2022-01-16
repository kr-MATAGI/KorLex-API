import pyodbc # MS Access (*.mdb)
import pandas as pd
from xml.etree import ElementTree as elemTree
import json
import copy

## Not Built-in
from korLexDef import *


### METHOD ###
def _local_db_connect(mdb_path:str=None):
    if mdb_path is None:
        print("[_local_db_connect]ERR - mdb_path is None !")
        return None, None

    print("DB Conn:", mdb_path)
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+mdb_path+';')
    cursor = conn.cursor()

    return conn, cursor

def search_synset_info(conn:pyodbc.Connection=None, mdb_path:str=None, soff:str=None, pos:str=None,
                       ontology=ONTOLOGY.KORLEX.value):
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
        synset_query = KORLEX_QUERY.SEARCH_SSINFO.value % (ontology, soff)
    else:
        synset_query = (KORLEX_QUERY.SEARCH_POS_SSINFO.value) % (ontology, pos, soff)
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

def search_sibling_nodes(conn:pyodbc.Connection=None, ontology:str=ONTOLOGY.KORLEX.value, mdb_path:str=None, word:str=None):
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
    query = KORLEX_QUERY.SEARCH_SIBLING_NODE.value % (ontology, word)
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

def serach_relation_index_info(conn:pyodbc.Connection=None, mdb_path:str=None, soff:str=None,
                                     ontology:str=ONTOLOGY.KORLEX.value):
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
    query = KORLEX_QUERY.SEARCH_REL_IDX_BY_TRGELEM.value % (ontology, soff)
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

def make_korlex_tree_resource(word:str=None, ontology:str=ONTOLOGY.KORLEX.value, mdb_path:str=None):
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
    search_target_info = search_sibling_nodes(conn=conn, ontology=ontology, word=word, mdb_path=mdb_path)
    print(search_target_info)

    # Make Tree (format. json)
    for st_info in search_target_info:
        search_target_synset = search_synset_info(conn=conn, soff=st_info.soff, pos=st_info.pos, ontology=ontology)

        parent_json_data_list = []
        origin_json = KorLexJson(synset=[])
        origin_json.synset = [(st_info.word, st_info.senseId)]
        origin_json.soff = st_info.soff

        if 0 >= len(search_target_synset.parent_list):
            parent_json_data_list.append([origin_json])
        for target_parent in search_target_synset.parent_list:
            parent_json_data = []
            parent_json_data.append(origin_json)

            target_soff = target_parent
            target_pos = st_info.pos
            while None != target_soff:
                # Search Synset
                sysnset_data = search_synset_info(conn=conn, soff=target_soff, pos=target_pos, ontology=ontology)
                korlex_json = KorLexJson(synset=[])
                korlex_json.synset = sysnset_data.word_list
                korlex_json.soff = target_soff
                parent_json_data.append(korlex_json)

                # Search relation index
                prev_target_soff = target_soff
                target_soff = serach_relation_index_info(conn=conn, soff=target_soff, ontology=ontology)
                if prev_target_soff == target_soff:
                    break # Stop Loop
            parent_json_data_list.append(parent_json_data)
        ret_json_rsrc_list.append(parent_json_data_list)

    # DB close
    conn.close()

    print(ret_json_rsrc_list)
    return ret_json_rsrc_list


def make_korlex_result_json(json_rsrc_list:list, ontology:str=ONTOLOGY.KORLEX.value):
    json_dict = {
        "ontology": ontology,
        "search_word": "",
        "search_senseid": "",
        "results": []
    }

    # Make Dict
    for json_rsrc in json_rsrc_list:
        print(json_rsrc)
        if "" == json_dict["search_word"]:
            json_dict["search_word"] = json_rsrc[0].synset[0][0]
            json_dict["search_senseid"] = str(json_rsrc[0].synset[0][1])

        for rsrc_item in json_rsrc:
            item_dict = {
                "word_sets": [],
                "soff": rsrc_item.soff
            }

            for word in rsrc_item.synset:
                wordset_dict = {
                    "word": word[0],
                    "senseid": word[1]
                }
                item_dict["word_sets"].append(wordset_dict)
            json_dict["results"].append(item_dict)

    ret_json = json.dumps(json_dict, ensure_ascii=False).encode("utf8")

    return ret_json.decode()

def _make_word_to_synset_dict(conn:pyodbc.Connection=None, ontology:str=None):
    if (conn is None) or (ontology is None):
        if conn is None: print("[_make_word_to_synset_dict] conn is NULL")
        else: print("[_make_word_to_synset_dict] ontology is NULL")
        return

    # query
    query = KORLEX_QUERY.ALL_SE_IDX_BY_ONTOLOGY.value % ontology
    synset_word_info = pd.read_sql_query(query, conn)

    word2synset_dict, synset2word_dict = {}, {}
    for idx, row in synset_word_info.iterrows():
        word = row["fldWNI_WORD"]
        soff = int(row["fldWNI_SOFF"])

        word2synset_dict[word] = soff
        synset2word_dict[soff] = word

    return word2synset_dict, synset2word_dict

def _parse_field_xml_from_ssinfo(src_xml:str=""):
    ret_dict = {
        "syn": {
            "pos": "",
            "lexfn": "",
            "soff": -1,
            "descendent": -1
        },
        "gloss": "",
        "domain": "",
        "word": [],
        "pointer": []
    }

    # SYN
    syn_node = elemTree.fromstring(src_xml)
    ret_dict["syn"]["pos"] = syn_node.get("pos", "")
    ret_dict["syn"]["lexfn"] = syn_node.get("lexfn", "")
    ret_dict["syn"]["soff"] = int(syn_node.get("soff", -1))
    ret_dict["syn"]["descendent"] = int(syn_node.get("descendent", -1))

    # GLOSS
    gloss_node = syn_node.find("GLOSS")
    ret_dict["gloss"] = gloss_node.text

    # DOMAIN
    domain_block_node = syn_node.find("domainblock")
    domain_node = domain_block_node.find("domain")
    ret_dict["domain"] = domain_node.text

    # WORD
    word_dict = {
        "senseid": -1,
        "seq": -1,
        "text": ""
    }

    word_node_list = syn_node.findall("WORD")
    for word_node in word_node_list:
        word_dict["senseid"] = word_node.get("senseid", -1)
        word_dict["seq"] = word_node.get("seq", -1)
        word_dict["text"] = word_node.text
        ret_dict["word"].append(copy.deepcopy(word_dict))

    # POINTER
    pointer_dict = {
        "symbol": "",
        "tsoff": -1,
        "tpos": "",
    }

    pointer_node_list = syn_node.findall("POINTER")
    for pt_node in pointer_node_list:
        pointer_dict["symbol"] = pt_node.get("symbol", "")
        pointer_dict["tsoff"] = pt_node.get("tsoff", -1)
        pointer_dict["tpos"] = pt_node.get("tpos", "")
        ret_dict["pointer"].append(copy.deepcopy(pointer_dict))

    return ret_dict

def _make_realtion_info_from_table(conn:pyodbc.Connection=None, ontology:str=None, soff:str=None):
    ret_rel_info_dict_list = []

    query = KORLEX_QUERY.SEARCH_REL_IDX_BY_SOFF.value % (ontology, soff)
    rel_info_list = pd.read_sql_query(query, conn)

    rel_info_dict = {
        "ontology": "",
        "pos": "",
        "elem": -1,
        "senseid": -1,
        "relation": "",
        "trg": {
            "pos": "",
            "elem": -1,
            "senseid": -1,
        }
    }

    for idx, rel_info in rel_info_list.iterrows():
        rel_info_dict["ontology"] = rel_info.get("fldWNIR_ONTOLOGY", "")
        rel_info_dict["pos"] = rel_info.get("fldWNIR_POS", "")
        rel_info_dict["elem"] = int(rel_info.get("fldWNIR_ELEMENT", -1))
        rel_info_dict["senseid"] = int(rel_info.get("fldWNIR_SENSEID", -1))
        rel_info_dict["relation"] = rel_info.get("fldWNIR_RELATION", "")
        rel_info_dict["trg"]["pos"] = rel_info.get("fldWNIR_TRGPOS", "")
        rel_info_dict["trg"]["elem"] = int(rel_info.get("fldWNIR_TRGELEMENT", -1))
        rel_info_dict["trg"]["senseid"] = int(rel_info.get("fldWNIR_TRGSENSEID", -1))

        ret_rel_info_dict_list.append(copy.deepcopy(rel_info_dict))

    return ret_rel_info_dict_list

def _make_all_info_dict(conn:pyodbc.Connection=None, ontology:str=None):
    if (conn is None) or (ontology is None):
        if conn is None: print("[_make_all_ss_info_dict] conn is NULL")
        else: print("[_make_all_ss_info_dict] ontology is NULL")
        return

    query = KORLEX_QUERY.ALL_SS_INFO_BY_ONTOLOGY.value % ontology
    all_ss_info = pd.read_sql_query(query, conn)

    ret_ss_info_dict = {}
    for idx, row in all_ss_info.iterrows():
        if 0 == (idx % 100):
            print("Processing... ", idx)

        fld_xml = row["fldXml"]
        fld_pos = row["fldPos"]
        fld_soff = int(row["fldSoff"]) # key
        fld_LexFn = row["fldLexFn"]

        # Parse fldXml
        fld_xml_dict = _parse_field_xml_from_ssinfo(src_xml=fld_xml)

        ret_ss_info_dict[fld_soff] = {
            "pos": fld_pos,
            "lexFn": fld_LexFn.strip(),
            "synset_info": fld_xml_dict,
            "relation_info": []
        }

        # Get relation info
        rel_info_dict_list = _make_realtion_info_from_table(conn=conn, ontology=ontology, soff=row["fldSoff"])
        ret_ss_info_dict[fld_soff]["relation_info"] = rel_info_dict_list

    return ret_ss_info_dict

def make_synset_dictionary(mdb_path:str=None, ontology=ONTOLOGY.KORLEX.value, dest_path:str=None):
    print("Start Make Synset Dictionary !")

    if (mdb_path is None) or (dest_path is None):
        print(f"[make_synset_dictionary] ERR - path is NULL, mdb:{mdb_path}, dest:{dest_path}")
        return

    # DB Connect
    conn, cursor = _local_db_connect(mdb_path=mdb_path)

    # make word2synset, synset2word dictionary
    word2ss_dict, ss2word_dict = _make_word_to_synset_dict(conn=conn, ontology=ontology)

    # save json file
    word2ss_file = ontology.lower() + "_word2ss.json"
    with open(dest_path+"/"+word2ss_file, "w") as outfile:
        json.dump(word2ss_dict, outfile)

    ss2word_file = ontology.lower() + "_ss2word.json"
    with open(dest_path+"/"+ss2word_file, "w") as outfile:
        json.dump(ss2word_dict, outfile)

    # make all info dictionary
    all_info_dict = _make_all_info_dict(conn=conn, ontology=ontology)

    # save json file
    all_info_file = ontology.lower() + "_all_info.json"
    with open(dest_path+"/"+all_info_file, "w") as outfile:
        json.dump(all_info_dict, outfile)


### TEST ###
if "__main__" == __name__:
    mdb_path = "../db/20170726_KorLexDB.mdb"
    '''
    json_rsc_list = make_korlex_tree_resource(word="eat",
                                              ontology=ONTOLOGY.WORDNET.value,
                                              mdb_path=mdb_path)

    for json_rsrc in json_rsc_list:
        test_res = make_korlex_result_json(json_rsrc)
        print(test_res)
        print()
    '''

    make_synset_dictionary(mdb_path=mdb_path, ontology=ONTOLOGY.KORLEX.value, dest_path="./dic")