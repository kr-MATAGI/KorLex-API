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
    def __init__(self, json_path:str, seIdx_path:str, reIdx_path:str):
        print("[KorLexAPI][INIT] Plz Wait...")

        self.is_set_json_path = False
        self.is_set_seIdx_path = False
        self.is_set_reIdx_path = False

        # check seIdx_path
        if 0 >= len(seIdx_path):
            print("[KorLexAPI][INIT] ERR - Plz check seIdx_path:", seIdx_path)
            return
        if not os.path.exists(seIdx_path):
            print("[KorLexAPI][INIT] ERR -", seIdx_path, "is Not Existed !")
            return

        self.seIdx_path = seIdx_path
        self.is_set_seIdx_path = True

        # check reIdx_path
        if 0 >= len(reIdx_path):
            print("[KorLexAPI][INIT] ERR - Plz check reIdx_path:", reIdx_path)
            return
        if not os.path.exists(reIdx_path):
            print("[KorLexAPI][INIT] ERR -", reIdx_path, "is Not Existed !")
            return

        self.reIdx_path = reIdx_path
        self.is_set_reIdx_path = True

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

        if not self.is_set_reIdx_path:
            print("[KorLexAPI][load_json_data] ERR - Plz set reIdx path")
            is_set_json_path = False

        if not is_set_json_path: return

        # Load seIdx.pkl ontology.json files
        print("[KorLexAPI][load_json_data] Loading seIdx.pkl...")
        self.seIdx_df = None
        with open(self.seIdx_path, mode="rb") as seIdx_file:
            self.seIdx_df = pickle.load(seIdx_file)
            print("[KorLexAPI][load_json_data] Loaded seIdx.pkl !")

        # Load seIdx.pkl ontology.json files
        print("[KorLexAPI][load_json_data] Loading reIdx.pkl...")
        self.reIdx_df = None
        with open(self.reIdx_path, mode="rb") as reIdx_file:
            self.reIdx_df = pickle.load(reIdx_file)
            print("[KorLexAPI][load_json_data] Loaded reIdx.pkl !")

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
    reIdx_path = "./dic/korlex_reIdx.pkl"
    krx_json_api = KorLexAPI(json_path=json_path,
                             seIdx_path=seIdx_path,
                             reIdx_path=reIdx_path)
    krx_json_api.load_json_data()

    import time
    start_time = time.time()
    krx_json_api.search_word(word="사과", ontology=ONTOLOGY.KORLEX.value)
    end_time = time.time()

    print(end_time - start_time)