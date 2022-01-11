from dataclasses import dataclass
from enum import Enum

class ONTOLOGY(Enum):
    KORLEX = "KORLEX"
    WORDNET = "WORDNET"
    FRNEWN = "FRNEWN"
    JPNWN = "JPNWN"
    PWN3 = "PWN3.0"

class KORLEX_QUERY(Enum):
    SEARCH_SIBLING_NODE = """
        SELECT * FROM 
        tblWN_SEIndex 
        WHERE fldWNI_ONTOLOGY = '%s'  
        AND fldWNI_WORD like '%s';
    """

    SEARCH_POS_SSINFO = """
        SELECT * FROM 
        tblWN_SSInfo 
        WHERE fldOntology = '%s' 
        AND fldPOS = '%s' 
        AND fldSoff like '%s';
    """

    SEARCH_SSINFO = """
            SELECT * FROM 
            tblWN_SSInfo 
            WHERE fldOntology = '%s' 
            AND fldSoff like '%s';
        """

    SEARCH_REL_IDX = """
        SELECT * FROM 
        tblWN_RelIndex 
        WHERE fldWNIR_ONTOLOGY = '%s'  
        AND fldWNIR_TRGELEMENT LIKE '%s';
    """

@dataclass
class SiblingNode:
    ontology: str = None
    pos: str = None
    soff: str = None
    word: str = None
    senseId: str = None

@dataclass
class SynsetData:
    word_list: list()
    parent_list: list()
    child_list: list()

@dataclass
class KorLexJson:
    synset: list()
    soff: str = ""
