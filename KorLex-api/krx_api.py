import time
import pickle
import pandas as pd
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

    def _make_sibling_list(self, soff:int, pos:str):
        ret_sibling_list = []

        target_re_idx_list = np.where((self.reIdx_df["elem"].values == soff) &
                                        (self.reIdx_df["relation"].values == "child") &
                                        (self.reIdx_df["trg_pos"].values == pos))
        for t_elem_re_idx in target_re_idx_list:
            for _, reIdx_item in self.reIdx_df.loc[t_elem_re_idx].iterrows():
                trg_elem = reIdx_item["trg_elem"]
                trg_elem_seIdx_list = np.where((self.seIdx_df["soff"].values == trg_elem) &
                                               (self.seIdx_df["pos"].values == pos))

                for t_elem_se_idx in trg_elem_seIdx_list:
                    se_ss_node = SS_Node([], soff=trg_elem, pos=pos)
                    for _, seIdx_item in self.seIdx_df.loc[t_elem_se_idx].iterrows():
                        se_synset = Synset(text=seIdx_item["word"],
                                           sense_id=seIdx_item["senseid"])
                        se_ss_node.synset_list.append(copy.deepcopy(se_synset))
                    ret_sibling_list.append(copy.deepcopy(se_ss_node))

        return ret_sibling_list

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
                                                  soff=target_obj["soff"]), [], [])

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

            sibling_list = self._make_sibling_list(soff=target_obj["soff"], pos=target_obj["pos"])
            result_data.siblings = copy.deepcopy(sibling_list)

            ret_korlex_result_list.append(result_data)

        # Existed Parent
        for target_parent in target_parent_list:
            # set target info
            result_data = KorLexResult(Target(ontology=ontology,
                                                  word=target_obj["word"],
                                                  pos=target_obj["pos"],
                                                  sense_id=target_obj["senseid"],
                                                  soff=target_obj["soff"]), [], [])

            ## Search processing
            curr_target = (target_parent[0], target_parent[-1])

            # current target synset
            curr_ss_node = SS_Node(synset_list=[], soff=target_obj["soff"], pos=target_obj["pos"])
            curr_se_matcing_list = np.where((self.seIdx_df["soff"].values == target_obj["soff"]) &
                                            (self.seIdx_df["pos"].values == target_obj["pos"]))

            for curr_se_idx in curr_se_matcing_list:
                for _, curr_se_item in self.seIdx_df.loc[curr_se_idx].iterrows():
                    curr_seIdx_word = curr_se_item["word"]
                    curr_seIdx_senseId = curr_se_item["senseid"]
                    curr_synset_data = Synset(text=curr_seIdx_word, sense_id=curr_seIdx_senseId)
                    curr_ss_node.synset_list.append(copy.deepcopy(curr_synset_data))
            result_data.results.append(curr_ss_node)

            # search sibling for target
            sibling_list = self._make_sibling_list(soff=curr_target[0], pos=curr_target[-1])
            result_data.siblings = copy.deepcopy(sibling_list)

            # search loop
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
        ret_json_list = []

        if 0 >= len(word):
            print("[KorLexAPI][search_word] ERR - Check input:", word)
            return ret_json_list

        if word not in self.seIdx_df["word"].values:
            print("[KorLexAPI][search_word] ERR - Not Existed SE Index Table:", word)
            return ret_json_list

        # Search sibling nodes
        sibling_idx_list = np.where(self.seIdx_df["word"].values == word)
        sibling_obj_list = []
        for sIdx in sibling_idx_list[0]:
            sibling_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        # Make Result Json
        for target_obj in sibling_obj_list:
            target_krx_json = self._make_result_json(target_obj=target_obj, ontology=ontology)
            ret_json_list.append(copy.deepcopy(target_krx_json))

        return ret_json_list

    def search_synset(self, synset:str, ontology:str):
        ret_json_list = []

        if 0 >= len(synset):
            print("[KorLexAPI][search_synset] ERR - Check input:", synset)
            return ret_json_list

        synset = int(synset)
        if synset not in self.seIdx_df["soff"].values:
            print("[KorLexAPI][search_synset] ERR - Not Existed SE Index Table:", synset)
            return ret_json_list

        # Search sibling nodes
        sibling_idx_list = np.where(self.seIdx_df["soff"].values == synset)
        sibling_obj_list = []
        for sIdx in sibling_idx_list[0]:
            sibling_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        # Make Result Json
        for target_obj in sibling_obj_list:
            target_krx_json = self._make_result_json(target_obj=target_obj, ontology=ontology)
            ret_json_list.append(copy.deepcopy(target_krx_json))

        return ret_json_list

    # WIKI
    def load_wiki_relation(self, wiki_rel_path:str):
        self.wiki_df = None

        if not os.path.exists(wiki_rel_path):
            print("[KorLexAPI][load_wiki_relation] ERR - Plz Check wiki_rel_path:", wiki_rel_path)
            return

        with open(wiki_rel_path, mode="r", encoding="cp949") as wiki_rel_file:
            word_list = []
            sysnet_list = []
            for line in wiki_rel_file.readlines():
                split_line = line.strip().split(",")
                sysnet = split_line[0]
                sysnet_list.append(sysnet)

                word = split_line[-1]
                word_list.append(word)
            self.wiki_df = pd.DataFrame((word_list, sysnet_list), index=["word", "synset"]).transpose()

    def search_wiki_word(self, word:str, ontology:str):
        ret_target_list = []
        ret_related_list = []

        if 0 >= len(word):
            print("[KorLexAPI][search_wiki_word] ERR - Word is NULL word:", word)
            return ret_target_list, ret_related_list
        if self.wiki_df is None:
            print("[KorLexAPI][search_wiki_word] ERR - self.wiki_df is None !")
            return ret_target_list, ret_related_list

        # Convert wiki word to synset num
        total_result_list = []
        target_wiki_rel_list = np.where(self.wiki_df["word"].values == word)
        for t_wiki_rel_idx in target_wiki_rel_list:
            for _, wiki_rel_item in self.wiki_df.loc[t_wiki_rel_idx].iterrows():
                wiki_rel_synset = wiki_rel_item["synset"]
                wiki_rel_result = self.search_synset(synset=wiki_rel_synset, ontology=ontology)
                if wiki_rel_result is not None:
                    total_result_list.extend(copy.deepcopy(wiki_rel_result))

        for result in total_result_list:
            if word == result[0].target.word:
                ret_target_list.extend(copy.deepcopy(result))
            else:
                ret_related_list.extend(copy.deepcopy(result))

        return ret_target_list, ret_related_list

### TEST ###
if "__main__" == __name__:
    ssInfo_path = "./dic/korlex_ssInfo.pkl"
    seIdx_path = "./dic/korlex_seIdx.pkl"
    reIdx_path = "./dic/korlex_reIdx.pkl"
    krx_json_api = KorLexAPI(ssInfo_path=ssInfo_path,
                             seIdx_path=seIdx_path,
                             reIdx_path=reIdx_path)
    krx_json_api.load_synset_data()

    test_search_synset = krx_json_api.search_word(word="먹다", ontology=ONTOLOGY.KORLEX.value)
    for t_s in test_search_synset:
        print(t_s)
    exit()

    # if you want to use wiki relation, write below methods
    wiki_rel_path = "./wiki/pwn2.0_krwiki.txt"
    krx_json_api.load_wiki_relation(wiki_rel_path=wiki_rel_path)

    start_time = time.time()
    target_result, related_result = krx_json_api.search_wiki_word(word="의사", ontology=ONTOLOGY.KORLEX.value)
    end_time = time.time()

    for t_r in target_result:
        print(t_r)
    print()
    for r_r in related_result:
        print(r_r)

    print("proc time:", end_time - start_time)