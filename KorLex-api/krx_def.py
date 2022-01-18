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

    SEARCH_REL_IDX_BY_TRGELEM = """
        SELECT * FROM 
        tblWN_RelIndex 
        WHERE fldWNIR_ONTOLOGY = '%s'  
        AND fldWNIR_TRGELEMENT LIKE '%s';
    """

    SEARCH_REL_IDX_BY_SOFF = """
        SELECT * FROM
        tblWN_RelIndex
        WHERE fldWNIR_ONTOLOGY = '%s'
        AND fldWNIR_ELEMENT LIKE '%s';
    """

    ALL_REL_IDX_BY_ONTOLOGY = """
        SELECT * FROM
        tblWN_RelIndex
        WHERE fldWNIR_ONTOLOGY = '%s';
    """

    ALL_SE_IDX_BY_ONTOLOGY = """
        SELECT * FROM  
        tblWN_SEIndex 
        WHERE fldWNI_ONTOLOGY = '%s';
    """

    ALL_SS_INFO_BY_ONTOLOGY = """
        SELECT fldXml, fldPos, fldSoff, fldLexFn FROM 
        tblWN_SSINFO 
        WHERE fldOntology = '%s';
    """


@dataclass
class Target:
    ontology: str = ""
    word: str = ""
    sense_id: str = ""
    pos: str = ""
    soff: int = -1

@dataclass
class Synset:
    text: str = ""
    sense_id: str = ""

@dataclass
class SS_Node:
    synset_list: list() # Synset
    soff: int = -1
    pos: str = ""

@dataclass
class KorLexResult:
    target: Target()
    results: list() # SS_Node
    siblings: list() # SS_Node
