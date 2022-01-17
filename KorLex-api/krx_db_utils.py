import pyodbc # MS Access (*.mdb)
import pandas as pd
from xml.etree import ElementTree as elemTree
import json
import copy
import pickle

## KorLex API Json Definition
from korLexDef import *

### Class
class KorLexDB_Utils:
    ### PRVIATE ###
    def _local_db_connect(self, mdb_path: str = None):
        '''
        Connection *.mdb file by using ms access driver (pyodbc).
        * recommend use in 'windows' env.
        :param mdb_path: korlex ms access local file path (*.mdb)
        :return: conn:pyodbc.Connection, cursor:pyodbc.Cursor
        '''
        if mdb_path is None:
            print("[_local_db_connect]ERR - mdb_path is None !")
            return None, None

        print("DB Conn:", mdb_path)
        conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + mdb_path + ';')
        cursor = conn.cursor()

        return conn, cursor

    def _make_word_to_synset_dict(self, conn: pyodbc.Connection = None, ontology: str = None):
        '''
        :param conn: connection obj of *.mdb
        :param ontology: KorLexDef.ONTOLOGY(Enum)
        :return: word2synset_dict, synset2word_dict
        '''
        if (conn is None) or (ontology is None):
            if conn is None:
                print("[_make_word_to_synset_dict] conn is NULL")
            else:
                print("[_make_word_to_synset_dict] ontology is NULL")
            return

        # query
        query = KORLEX_QUERY.ALL_SE_IDX_BY_ONTOLOGY.value % ontology
        synset_word_info = pd.read_sql_query(query, conn)

        word_list = []
        soff_list = []
        senseid_list = []
        pos_list = []
        for idx, row in synset_word_info.iterrows():
            word = row["fldWNI_WORD"]
            soff = int(row["fldWNI_SOFF"])
            senseid = row["fldWNI_SENSEID"]
            pos = row["fldWNI_POS"]

            word_list.append(word)
            soff_list.append(soff)
            senseid_list.append(senseid)
            pos_list.append(pos)

        seIdx_df = pd.DataFrame((word_list, soff_list, senseid_list, pos_list),
                                 index=["word", "soff", "senseid", "pos"]).transpose()
        return seIdx_df

    def _make_rel_idx_dict(self, conn: pyodbc.Connection = None, ontology: str = None):
        if (conn is None) or (ontology is None):
            if conn is None:
                print("[_make_word_to_synset_dict] conn is NULL")
            else:
                print("[_make_word_to_synset_dict] ontology is NULL")
            return

        # query
        query = KORLEX_QUERY.ALL_REL_IDX_BY_ONTOLOGY.value % ontology
        rel_idx_rows = pd.read_sql_query(query, conn)

        # make
        pos_list = []
        element_list = []
        senseid_list = []
        relation_list = []

        trg_pos_list = []
        trg_element_list = []
        trg_senseid_list = []
        for idx, row in rel_idx_rows.iterrows():
            pos = row["fldWNIR_POS"]
            try:
                element = int(row["fldWNIR_ELEMENT"])
            except:
                print(row["fldWNIR_ELEMENT"], "ERR - elem")
                continue
            senseid = row["fldWNIR_SENSEID"]
            relation = row["fldWNIR_RELATION"]
            trg_pos = row["fldWNIR_TRGPOS"]

            try:
                trg_element = int(row["fldWNIR_TRGELEMENT"])
            except:
                print(row["fldWNIR_TRGELEMENT"], "ERR - trg elem")
                continue
            trg_senseid = row["fldWNIR_TRGSENSEID"]

            pos_list.append(pos)
            element_list.append(element)
            senseid_list.append(senseid)
            relation_list.append(relation)
            trg_pos_list.append(trg_pos)
            trg_element_list.append(trg_element)
            trg_senseid_list.append(trg_senseid)

        make_list_set = (pos_list, element_list, senseid_list, relation_list, trg_pos_list,
                         trg_element_list, trg_senseid_list)
        rel_idx_df = pd.DataFrame(make_list_set, index=["pos", "elem", "senseid", "relation",
                                                       "trg_pos", "trg_elem", "trg_senseid"]).transpose()
        return rel_idx_df

    def _make_ss_info_dict(self, conn: pyodbc.Connection = None, ontology: str = None):
        if (conn is None) or (ontology is None):
            if conn is None:
                print("[_make_word_to_synset_dict] conn is NULL")
            else:
                print("[_make_word_to_synset_dict] ontology is NULL")
            return

        # query
        query = KORLEX_QUERY.ALL_SS_INFO_BY_ONTOLOGY.value % ontology
        ss_info_rows = pd.read_sql_query(query, conn)

        # make
        pos_list = []
        soff_list = []
        lexFn_list = []
        for idx, row in ss_info_rows.iterrows():
            pos = row["fldPos"]
            soff = int(row["fldSoff"])
            lexFn = row["fldLexFn"]

            pos_list.append(pos)
            soff_list.append(soff)
            lexFn_list.append(lexFn)

        make_list_set = (pos_list, soff_list, lexFn_list)
        ss_info_df = pd.DataFrame(make_list_set, index=["pos", "soff", "lexFn"]).transpose()
        return ss_info_df

    def _parse_field_xml_from_ssinfo(self, src_xml: str = ""):
        '''
        :param: fildXml field data
        :return: parsed data (dictionary format)
        '''
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

    def _make_realtion_info_from_table(conn: pyodbc.Connection = None,
                                       ontology: str = None,
                                       soff: str = None):
        '''
        parse 'tlbWN_RelIndex' table
        :param ontology: KorLexDef.ONTOLOGY(Enum)
        :param soff: synset value
        :return: dictionary of tblWN_RelIndex table's data
        '''
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

    def _make_all_info_dict(self, conn: pyodbc.Connection = None, ontology: str = None):
        '''

        :param conn: connection obj of *.mdb
        :param ontology: KorLexDef.ONTOLOGY(Enum)
        :return: dictionary ('ssinfo table in db)
        '''
        if (conn is None) or (ontology is None):
            if conn is None:
                print("[_make_all_ss_info_dict] conn is NULL")
            else:
                print("[_make_all_ss_info_dict] ontology is NULL")
            return

        query = KORLEX_QUERY.ALL_SS_INFO_BY_ONTOLOGY.value % ontology
        all_ss_info = pd.read_sql_query(query, conn)

        ret_all_info_dict = {}
        for idx, row in all_ss_info.iterrows():
            if 0 == (idx % 100):
                print("Processing... ", idx)

            fld_xml = row["fldXml"]
            fld_pos = row["fldPos"]
            fld_soff = int(row["fldSoff"])  # key
            fld_LexFn = row["fldLexFn"]

            # Parse fldXml
            fld_xml_dict = self._parse_field_xml_from_ssinfo(src_xml=fld_xml)

            ret_all_info_dict[fld_soff] = {
                "pos": fld_pos,
                "lexFn": fld_LexFn.strip(),
                "synset_info": fld_xml_dict,
                "relation_info": []
            }

            # Get relation info
            rel_info_dict_list = self._make_realtion_info_from_table(conn=conn,
                                                                     ontology=ontology,
                                                                     soff=row["fldSoff"])
            ret_all_info_dict[fld_soff]["relation_info"] = rel_info_dict_list

        return ret_all_info_dict

    ### PULBIC ###
    # Make KorLex Json Dictionary
    def make_synset_dictionary(self,
                               mdb_path: str = None,
                               ontology: str = ONTOLOGY.KORLEX.value,
                               dest_path: str = None):
        '''
        :param mdb_path: mdb_path: korlex ms access local file path (*.mdb)
        :param ontology: KorLexDef.ONTOLOGY(Enum)
        :param dest_path: save path (write directory path)
        :return: None
        '''
        print("Start Make Synset Dictionary !")

        if (mdb_path is None) or (dest_path is None):
            print(f"[make_synset_dictionary] ERR - path is NULL, mdb:{mdb_path}, dest:{dest_path}")
            return

        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)

        # make word2synset, synset2word dictionary
        word2ss_dict, ss2word_dict = self._make_word_to_synset_dict(conn=conn, ontology=ontology)

        # save json file
        word2ss_file = ontology.lower() + "_word2ss.json"
        with open(dest_path + "/" + word2ss_file, "w") as outfile:
            json.dump(word2ss_dict, outfile)

        ss2word_file = ontology.lower() + "_ss2word.json"
        with open(dest_path + "/" + ss2word_file, "w") as outfile:
            json.dump(ss2word_dict, outfile)

        # make all info dictionary
        all_info_dict = self._make_all_info_dict(conn=conn, ontology=ontology)

        # save json file
        all_info_file = ontology.lower() + "_all_info.json"
        with open(dest_path + "/" + all_info_file, "w") as outfile:
            json.dump(all_info_dict, outfile)

    def make_seIndex_dictionary(self, mdb_path:str,
                                dest_path:str,
                                ontology:str=ONTOLOGY.KORLEX.value):
        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)

        # make synset_df
        seIdx_df = self._make_word_to_synset_dict(conn=conn, ontology=ontology)

        # save pkl file
        seIdx_file = ontology.lower() + "_seIdx.pkl"
        with open(dest_path + "/" + seIdx_file, mode="wb") as outfile:
            pickle.dump(seIdx_df, outfile)

    def make_rel_index_dictionary(self, mdb_path:str,
                                  dest_path:str,
                                  ontology:str=ONTOLOGY.KORLEX.value):

        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)
        # make rel_idx_df
        rel_idx_df = self._make_rel_idx_dict(conn=conn, ontology=ontology)

        rel_idx_file = ontology.lower() + "_reIdx.pkl"
        with open(dest_path + "/" + rel_idx_file, mode="wb") as outfile:
            pickle.dump(rel_idx_df, outfile)

    def make_ss_info_dictionary(self, mdb_path:str,
                                dest_path:str,
                                ontology:str=ONTOLOGY.KORLEX.value):

        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)

        # make ss_info_df (Except fldXML)
        ss_info_df = self._make_ss_info_dict(conn=conn, ontology=ontology)

        ss_info_file = ontology.lower() + "_ssInfo.pkl"
        with open(dest_path + "/" + ss_info_file, mode="wb") as outfile:
            pickle.dump(ss_info_df, outfile)

### TEST ###
if "__main__" == __name__:
    mdb_path = "../db/20170726_KorLexDB.mdb"

    krx_db_util = KorLexDB_Utils()
    # krx_db_util.make_synset_dictionary(mdb_path=mdb_path,
    #                                    ontology=ONTOLOGY.KORLEX.value,
    #                                    dest_path="./dic")

    krx_db_util.make_seIndex_dictionary(mdb_path=mdb_path,
                                        dest_path="./dic",
                                        ontology=ONTOLOGY.KORLEX.value)

    # krx_db_util.make_rel_index_dictionary(mdb_path=mdb_path,
    #                                       dest_path="./dic",
    #                                       ontology=ONTOLOGY.KORLEX.value)

    # krx_db_util.make_ss_info_dictionary(mdb_path=mdb_path,
    #                                     dest_path="./dic",
    #                                     ontology=ONTOLOGY.KORLEX.value)