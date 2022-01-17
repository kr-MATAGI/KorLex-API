import pandas as pd
import json
import pickle
import numpy as np
import copy
import os

## Korlex API Definition
from korLexDef import *

class KorLexAPI:
    ### PRIVATE ###
    ### METHOD ###
    def __init__(self, json_path:str, seIdx_path:str):
        print("[KorLexAPI][INIT] Plz Wait...")

        self.is_set_json_path = False
        self.is_set_seIdx_path = False

        # check seIdx_path
        if 0 >= len(seIdx_path):
            print("[KorLexAPI][INIT] ERR - Plz check seIdx_path:", seIdx_path)
            return
        if not os.path.exists(seIdx_path):
            print("[KorLexAPI][INIT] ERR -", seIdx_path, "is Not Existed !")
            return

        self.seIdx_path = seIdx_path
        self.is_set_seIdx_path = True

        # Check Json file path
        if 0 >= len(json_path):
            print("[KorLexAPI][INIT] ERR - Plz check jsonPath:", json_path)
            return

        if not os.path.exists(json_path):
            print("[KorLexAPI][INIT] ERR -", json_path, "is Not Existed !")
            return

        self.is_set_json_path = True
        self.json_path = json_path
        print("[KorLexAPI][INIT] - Complete set to path,", self.json_path,
              "you can use load method.")

    def _make_result_json(self, target_obj:object, ontology:str):
        # init
        ret_result_data = KorLexResult(Target(), [])
        ret_result_data.target.ontology = ontology

        target_word = target_obj["word"]
        target_soff = target_obj["soff"]
        target_senseId = target_obj["senseid"]
        ret_result_data.target.word = target_word

        # search target
        serach_result_json = self.krx_json[str(target_soff)]
        syn_pos = serach_result_json["synset_info"]["syn"]["pos"]
        syn_soff = serach_result_json["synset_info"]["syn"]["soff"]
        ret_result_data.target.pos = syn_pos

        # Syn word
        target_syn_word_list = serach_result_json["synset_info"]["word"]
        target_SS_Node = SS_Node([], soff=syn_soff, pos=syn_pos)
        for t_syn_word in target_syn_word_list:
            synset = Synset(sense_id=t_syn_word["senseid"],
                            seq=t_syn_word["seq"],
                            text=t_syn_word["text"])
            target_SS_Node.synset_list.append(copy.deepcopy(synset))

        # pointer info
        target_pointer_list = serach_result_json["synset_info"]["pointer"]
        target_parent_list = []
        for pt_info in target_pointer_list:
            if "parent" == pt_info["symbol"]:
                pt_val = int(pt_info["tsoff"])
                pt_pos = pt_info["tpos"]
                target_parent_list.append((pt_val, pt_pos))

        for parent_elem in target_parent_list:
            target_elem = parent_elem

            parent_result = []
            while True:
                prev_target_elem = target_elem
                elem_json = self.krx_json[str(target_elem[0])]
                elem_syn_word_list = elem_json["synset_info"]["word"]
                elem_soff = elem_json["synset_info"]["syn"]["soff"]
                elem_pos = elem_json["synset_info"]["syn"]["pos"]

                if(prev_target_elem[1] == elem_pos):
                    elem_SS_Node = SS_Node([], soff=elem_soff, pos=elem_pos)
                    for e_syn_word in elem_syn_word_list:
                        e_synset = Synset(sense_id=e_syn_word["senseid"],
                                        seq=e_syn_word["seq"],
                                        text=e_syn_word["text"])
                        elem_SS_Node.synset_list.append(copy.deepcopy(e_synset))
                    parent_result.append(copy.deepcopy(elem_SS_Node))

                elem_pt_list = elem_json["synset_info"]["pointer"]
                for elem_pt_info in elem_pt_list:
                    if ("parent" == elem_pt_info["symbol"]) and (prev_target_elem[1] == elem_pt_info["tpos"]):
                        e_val = int(elem_pt_info["tsoff"])
                        e_pos = elem_pt_info["tpos"]
                        target_elem = (e_val, e_pos)
                if prev_target_elem == target_elem:
                    print("BRE\n") # TEST
                    break

            # loop end
            parent_result.insert(0, target_SS_Node)
            print(parent_result)

        return ret_result_data

    ### PUBLIC ###
    def load_json_data(self):
        print("[KorLexAPI][load_json_data] Load JSON Data, Wait...")
        is_set_json_path = True
        if not self.is_set_json_path:
            print("[KorLexAPI][load_json_data] ERR - Plz set json path")
            is_set_json_path = False

        if not self.is_set_seIdx_path:
            print("[KorLexAPI][load_json_data] ERR - Plz set seIdx path")
            is_set_json_path = False

        if not is_set_json_path: return

        ## Load seIdx.pkl ontology.json files
        # load w2ss json
        print("[KorLexAPI][load_json_data] Loading seIdx.pkl...")
        self.seIdx_df = None
        with open(self.seIdx_path, mode="rb") as w2ss_file:
            self.seIdx_df = pickle.load(w2ss_file)
            print("[KorLexAPI][load_json_data] Loaded seIdx.pkl !")

        # Load ontology json
        print("[KorLexAPI][load_json_data] Loading ontology json...")
        with open(self.json_path, mode="r", encoding="utf-8") as json_file:
            self.krx_json = json.load(json_file)
            print("[KorLexAPI][load_json_data] Loaded ontology json !")

    def search_word(self, word:str, ontology=str):
        ret_json = None

        if 0 >= len(word):
            print("[KorLexAPI][search_word] ERR - Check input:", word)
            return ret_json

        if word not in self.seIdx_df["word"].values:
            print("[KorLexAPI][search_word] ERR - Not Existed SE Index Table:", word)

        # Search sibling nodes
        sibling_idx_list = np.where(self.seIdx_df["word"].values == word)
        sibling_obj_list = []
        for sIdx in sibling_idx_list[0]:
            sibling_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        # Make Result Json
        ret_json_list = []
        for target_obj in sibling_obj_list:
            target_krx_json = self._make_result_json(target_obj=target_obj, ontology=ontology)
            ret_json_list.append(copy.deepcopy(target_krx_json))

        return ret_json_list

### TEST ###
if "__main__" == __name__:
    json_path = "./dic/korlex_all_info.json"
    seIdx_path = "./dic/korlex_seIdx.pkl"
    krx_json_api = KorLexAPI(json_path=json_path,
                             seIdx_path=seIdx_path)
    krx_json_api.load_json_data()
    krx_json_api.search_word(word="사과", ontology=ONTOLOGY.KORLEX.value)