import time
import pickle
import numpy as np
import copy
import os

## Korlex API Definition
from krx_def import *

class KorLexAPI:
    ### PRIVATE ###
    def __init__(self, ssInfo_path:str, seIdx_path:str, reIdx_path:str):
        print("[KorLexAPI][INIT] Plz Wait...")

        self.is_set_ssInfo_path = False
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

        # Check ssinfo_path
        if 0 >= len(ssInfo_path):
            print("[KorLexAPI][INIT] ERR - Plz check ssInfo_path:", ssInfo_path)
            return

        if not os.path.exists(ssInfo_path):
            print("[KorLexAPI][INIT] ERR -", ssInfo_path, "is Not Existed !")
            return

        self.is_set_ssInfo_path = True
        self.ssInfo_path = ssInfo_path
        print("[KorLexAPI][INIT] - Complete set to path,", self.ssInfo_path,
              "you can use load method.")

    def _make_result_json(self, target_obj:object, ontology:str):
        ret_korlex_result_list = []

        # check, is target parent dobule?
        target_parent_list = []
        check_parent_list = np.where(self.reIdx_df["trg_elem"].values == target_obj["soff"])
        for pt_idx in check_parent_list:
            for _, pt_item in self.reIdx_df.loc[pt_idx].iterrows():
                pt_relation = pt_item["relation"]
                if "child" == pt_relation:
                    pt_elem = pt_item["elem"]
                    pt_pos = pt_item["pos"]
                    target_parent_list.append((pt_elem, pt_pos))

        if 0 >= len(target_parent_list): # Except (e.g. eat(convert to korean))
            result_data = KorLexResult(Target(ontology=ontology,
                                                  word=target_obj["word"],
                                                  pos=target_obj["pos"],
                                                  sense_id=target_obj["senseid"],
                                                  soff=target_obj["soff"]), [])

            ss_node = SS_Node(synset_list=[], soff=target_obj["soff"], pos=target_obj["pos"])
            seIdx_matching_list = np.where(self.seIdx_df["soff"].values == ss_node.soff)
            for mat_idx in seIdx_matching_list:
                for _, seIdx_item in self.seIdx_df.loc[mat_idx].iterrows():
                    seIdx_word = seIdx_item["word"]
                    seIdx_pos = seIdx_item["pos"]
                    seIdx_senseId = seIdx_item["senseid"]

                    if seIdx_pos == target_obj["pos"]:
                        synset_data = Synset(text=seIdx_word, sense_id=seIdx_senseId)
                        ss_node.synset_list.append(copy.deepcopy(synset_data))
            result_data.results.append(ss_node)
            ret_korlex_result_list.append(result_data)

        # Existed Parent
        for target_parent in target_parent_list:
            # set target info
            result_data = KorLexResult(Target(ontology=ontology,
                                                  word=target_obj["word"],
                                                  pos=target_obj["pos"],
                                                  sense_id=target_obj["senseid"],
                                                  soff=target_obj["soff"]), [])

            # Search processing
            curr_target = (target_parent[0], target_parent[-1])
            while True:
                prev_target = copy.deepcopy(curr_target)


                # Search synset
                ss_node = SS_Node(synset_list=[], soff=curr_target[0], pos=curr_target[-1])
                seIdx_matching_list = np.where(self.seIdx_df["soff"].values == curr_target[0])
                for mat_idx in seIdx_matching_list:
                    for _, seIdx_item in self.seIdx_df.loc[mat_idx].iterrows():
                        seIdx_word = seIdx_item["word"]
                        seIdx_pos = seIdx_item["pos"]
                        seIdx_senseId = seIdx_item["senseid"]

                        if seIdx_pos == curr_target[-1]:
                            synset_data = Synset(text=seIdx_word, sense_id=seIdx_senseId)
                            ss_node.synset_list.append(copy.deepcopy(synset_data))

                if 0 >= len(ss_node.synset_list):
                    break
                else:
                    result_data.results.append(copy.deepcopy(ss_node))

                # Search parent
                reIdx_matching_list = np.where(self.reIdx_df["trg_elem"].values == curr_target[0])
                for mat_idx in reIdx_matching_list:
                    for _, reIdx_item in self.reIdx_df.loc[mat_idx].iterrows():
                        reIdx_rel = reIdx_item["relation"]
                        reIdx_pos = reIdx_item["pos"]

                        if ("child" == reIdx_rel) and (reIdx_pos == curr_target[-1]):
                            reIdx_elem = reIdx_item["elem"]
                            curr_target = (reIdx_elem, reIdx_pos)
                            break

                if(prev_target[0] == curr_target[0]): break
            ret_korlex_result_list.append(copy.deepcopy(result_data))

        return ret_korlex_result_list

    ### PUBLIC ###
    def load_synset_data(self):
        print("[KorLexAPI][load_synset_data] Load JSON Data, Wait...")
        is_set_pkl_files = True
        if not self.is_set_ssInfo_path:
            print("[KorLexAPI][load_synset_data] ERR - Plz set json path")
            is_set_pkl_files = False

        if not self.is_set_seIdx_path:
            print("[KorLexAPI][load_synset_data] ERR - Plz set seIdx path")
            is_set_pkl_files = False

        if not self.is_set_reIdx_path:
            print("[KorLexAPI][load_synset_data] ERR - Plz set reIdx path")
            is_set_pkl_files = False

        if not is_set_pkl_files: return

        # Load seIdx.pkl
        print("[KorLexAPI][load_synset_data] Loading seIdx.pkl...")
        self.seIdx_df = None
        with open(self.seIdx_path, mode="rb") as seIdx_file:
            self.seIdx_df = pickle.load(seIdx_file)
            print("[KorLexAPI][load_synset_data] Loaded seIdx.pkl !")

        # Load reIdx.pkl
        print("[KorLexAPI][load_synset_data] Loading reIdx.pkl...")
        self.reIdx_df = None
        with open(self.reIdx_path, mode="rb") as reIdx_file:
            self.reIdx_df = pickle.load(reIdx_file)
            print("[KorLexAPI][load_synset_data] Loaded reIdx.pkl !")

        # Load ssInfo
        print("[KorLexAPI][load_synset_data] Loading ssInfo.pkl...")
        self.ssInfo_df = None
        with open(self.ssInfo_path, mode="rb") as ssInfo_file:
            self.ssInfo_df = pickle.load(ssInfo_file)
            print("[KorLexAPI][load_synset_data] Loaded ssInfo.pkl !")

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
    ssInfo_path = "./dic/korlex_ssInfo.pkl"
    seIdx_path = "./dic/korlex_seIdx.pkl"
    reIdx_path = "./dic/korlex_reIdx.pkl"
    krx_json_api = KorLexAPI(ssInfo_path=ssInfo_path,
                             seIdx_path=seIdx_path,
                             reIdx_path=reIdx_path)
    krx_json_api.load_synset_data()

    # Check processing time
    start_time = time.time()
    results = krx_json_api.search_word(word="사과", ontology=ONTOLOGY.KORLEX.value)
    print(results)
    end_time = time.time()

    print(end_time - start_time)