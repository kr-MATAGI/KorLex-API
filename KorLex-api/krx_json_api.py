import pandas as pd
from xml.etree import ElementTree as elemTree
import json
import copy
import os
import sys

## Korlex API Definition
from korLexDef import *


class KorLexAPI:
    ### PRIVATE ###
    ### METHOD ###
    def __init__(self, json_path:str, w2ss_path:str, ss2w_path:str):
        print("[KorLexAPI][INIT] Plz Wait...")

        self.is_set_json_path = False
        self.is_set_w2ss_path = False
        self.is_set_ss2w_path = False

        # check w2ss_path, ss2w_path
        if 0 >= len(w2ss_path):
            print("[KorLexAPI][INIT] ERR - Plz check w2ss_path:", w2ss_path)
            return
        if not os.path.exists(w2ss_path):
            print("[KorLexAPI][INIT] ERR -", w2ss_path, "is Not Existed !")
            return

        if 0 >= len(ss2w_path):
            print("[KorLexAPI][INIT] ERR - Plz check ss2w_path:", ss2w_path)
            return
        if not os.path.exists(ss2w_path):
            print("[KorLexAPI][INIT] ERR -", ss2w_path, "is Not Existed !")
            return

        self.w2ss_path = w2ss_path
        self.ss2w_path = ss2w_path
        self.is_set_w2ss_path = True
        self.is_set_ss2w_path = True

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

    ### PUBLIC ###
    def load_json_data(self):
        print("[KorLexAPI][load_json_data] Load JSON Data, Wait...")
        is_set_json_path = True
        if not self.is_set_json_path:
            print("[KorLexAPI][load_json_data] ERR - Plz set json path")
            is_set_json_path = False

        if not self.is_set_w2ss_path:
            print("[KorLexAPI][load_json_data] ERR - Plz set w2ss path")
            is_set_json_path = False

        if not self.is_set_json_path:
            print("[KorLexAPI][load_json_data] ERR - Plz set ss2w path")
            is_set_json_path = False

        if not is_set_json_path: return

        ## Load w2ss, ss2w json files
        # load w2ss json
        print("[KorLexAPI][load_json_data] Loading w2ss json...")
        with open(self.w2ss_path, mode="r", encoding="utf-8") as w2ss_file:
            self.w2ss_json = json.load(w2ss_file)
            print("[KorLexAPI][load_json_data] Loaded w2ss json !")

        # load ss2w json
        print("[KorLexAPI][load_json_data] Loading ss2w json...")
        with open(self.ss2w_path, mode="r", encoding="utf-8") as ss2w_file:
            self.ss2w_json = json.load(ss2w_file)
            print("[KorLexAPI][load_json_data] Loaded ss2w json !")

        # Load ontolody json
        print("[KorLexAPI][load_json_data] Loading ontology json...")
        with open(self.json_path, mode="r", encoding="utf-8") as json_file:
            self.krx_json = json.load(json_file)
            print("[KorLexAPI][load_json_data] Loaded ontology json !")

    def search_word(self, word:str):
        ret_json = None
        # Convert synset (soff)
        if word not in self.w2ss_json.keys():
            print("[KorLexAPI][search_word] ERR - Not in w2ss:", word)
            return ret_json

        target_soff = self.w2ss_json[word]
        ret_json = self.search_synset(target_synset=target_soff)

        return ret_json

    def search_synset(self, target_synset):
        '''
        :param synset: is available str or int type
        :return:
        '''

        # init
        ret_json = None

        # Check synset param's type
        if type(target_synset) is str:
            try:
                target_synset = int(target_synset)
            except Exception as err:
                print("[KorLexAPI][search_synset] ERR - type convert:\n", err)

        return ret_json

### TEST ###
if "__main__" == __name__:
    json_path = "./dic/test.json"
    krx_json_api = KorLexAPI(json_path=json_path,
                             w2ss_path="",
                             ss2w_path="")
    krx_json_api.load_json_data()
