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
    def __init__(self, json_path:str):
        self.is_set_json_path = False

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
        if not self.is_set_json_path:
            print("[KorLexAPI][load_json_data] ERR - Plz set json path")
            return

        with open(self.json_path, mode="r", encoding="utf-8") as json_file:
            self.krx_json = json.load(json_file)

        print("[KorLexAPI][load_json_data] Complete load json data.")

    def TEST(self):
        print(self.krx_json)

### TEST ###
if "__main__" == __name__:
    json_path = "./dic/test.json"
    krx_json_api = KorLexAPI(json_path=json_path)
    krx_json_api.load_json_data()
    krx_json_api.TEST()
