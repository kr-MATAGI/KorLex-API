import pyodbc # MS Access (*.mdb)
import pandas as pd
import pickle
from typing import List

## KorLex API Definition
from krx_def import *

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

    def _make_word_seIdx_dict(self, conn: pyodbc.Connection = None, ontology: str = None):
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

    def _make_mapping_kwn_std_dict(self, conn: pyodbc.Connection=None):
        if conn is None:
            if conn is None:
                print("[_make_mapping_kwn_std_dict] conn is NULL")
            else:
                print("[_make_mapping_kwn_std_dict] ontology is NULL")
            return

        # query
        query = KORLEX_QUERY.ALL_MAPPING_KWN_STD_BY_ONTOLOGY.value
        kwn_std_rows = pd.read_sql_query(query, conn)

        # Make Simple
        soff_list = []
        ss_type_list = []
        korean_list = []
        sense_id_list = []
        std_idx_list = []
        std_num_list: List[str] = [] # fldStdidx1
        for idx, row in kwn_std_rows.iterrows():
            soff = row["fldSynsetOffset"]
            ss_type = row["fldSsType"]
            korean = row["fldKorean"]
            sense_id = row["fldSenseId"]
            std_idx = row["fldStdidx"]
            std_num = row["fldStdidx1"]

            soff_list.append(soff)
            ss_type_list.append(ss_type)
            korean_list.append(korean)
            sense_id_list.append(sense_id)
            std_idx_list.append(std_idx)
            std_num_list.append(str(std_num) if -1 != std_num else "00")

        make_list_set = (soff_list, ss_type_list, korean_list, sense_id_list, std_idx_list, std_num_list)
        index_title = ["soff", "ss_type", "korean", "senseid", "std_idx", "std_num"]
        kwn_std_df = pd.DataFrame(make_list_set, index=index_title).transpose()
        return kwn_std_df

    ### PULBIC ###
    def make_seIndex_dictionary(self, mdb_path:str,
                                dest_path:str,
                                ontology:str=ONTOLOGY.KORLEX.value):
        print("[krx_db_utils][make_seIndex_dictionary] - START -")
        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)

        # make synset_df
        seIdx_df = self._make_word_seIdx_dict(conn=conn, ontology=ontology)

        # save pkl file
        seIdx_file = ontology.lower() + "_seIdx.pkl"
        with open(dest_path + "/" + seIdx_file, mode="wb") as outfile:
            pickle.dump(seIdx_df, outfile)
            print("[krx_db_utils][make_seIndex_dictionary] - Save File -")
        print("[krx_db_utils][make_seIndex_dictionary] - Complete -")

    def make_rel_index_dictionary(self, mdb_path:str,
                                  dest_path:str,
                                  ontology:str=ONTOLOGY.KORLEX.value):
        print("[krx_db_utils][make_rel_index_dictionary] - START -")
        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)
        # make rel_idx_df
        rel_idx_df = self._make_rel_idx_dict(conn=conn, ontology=ontology)

        rel_idx_file = ontology.lower() + "_reIdx.pkl"
        with open(dest_path + "/" + rel_idx_file, mode="wb") as outfile:
            pickle.dump(rel_idx_df, outfile)
            print("[krx_db_utils][make_rel_index_dictionary] - Save File -")
        print("[krx_db_utils][make_rel_index_dictionary] - Complete -")

    def make_ss_info_dictionary(self, mdb_path:str,
                                dest_path:str,
                                ontology:str=ONTOLOGY.KORLEX.value):
        print("[krx_db_utils][make_ss_info_dictionary] - START -")
        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)

        # make ss_info_df (Except fldXML)
        ss_info_df = self._make_ss_info_dict(conn=conn, ontology=ontology)

        ss_info_file = ontology.lower() + "_ssInfo.pkl"
        with open(dest_path + "/" + ss_info_file, mode="wb") as outfile:
            pickle.dump(ss_info_df, outfile)
            print("[krx_db_utils][make_ss_info_dictionary] - Save File -")
        print("[krx_db_utils][make_ss_info_dictionary] - Complete -")

    def make_mapping_kwn_std(self, mdb_path: str,
                             dest_path: str,
                             ontology:str=ONTOLOGY.KORLEX.value):
        print("[krx_db_utils][make_mapping_kwn_std] - START -")
        # DB Connect
        conn, cursor = self._local_db_connect(mdb_path=mdb_path)

        # make kwn_std_df
        kwn_std_df = self._make_mapping_kwn_std_dict(conn=conn)

        # save pkl file
        kwn_std_file = ontology.lower() + "_kwn_std.pkl"
        with open(dest_path + "/" + kwn_std_file, mode="wb") as outfile:
            pickle.dump(kwn_std_df, outfile)
            print("[krx_db_utils][make_mapping_kwn_std] - Save File -")
        print("[krx_db_utils][make_mapping_kwn_std] - Complete -")

### TEST ###
if "__main__" == __name__:
    mdb_path = "C:/Users/MATAGI/Desktop/Git/KorLex-API/KorLex-api/db/std_dic.mdb"

    krx_db_util = KorLexDB_Utils()

    krx_db_util.make_mapping_kwn_std(mdb_path=mdb_path,
                                     dest_path="./dic")

    krx_db_util.make_seIndex_dictionary(mdb_path=mdb_path,
                                        dest_path="./dic",
                                        ontology=ONTOLOGY.KORLEX.value)

    krx_db_util.make_rel_index_dictionary(mdb_path=mdb_path,
                                          dest_path="./dic",
                                          ontology=ONTOLOGY.KORLEX.value)

    krx_db_util.make_ss_info_dictionary(mdb_path=mdb_path,
                                        dest_path="./dic",
                                        ontology=ONTOLOGY.KORLEX.value)