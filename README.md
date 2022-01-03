# KorLex-Read-API
  - 


## Table Structure (\[localdb\].mdb)
  <b>1. tblWN_ELEMENTS</b>
   
   | 필드 이름 | 데이터 형식 |
   | :----: | :----: |
   | fldWNE_ONTOLOGY | 짧은 텍스트 |
   | fldWNE_POS | 짧은 텍스트 |
   | fldWNE_SEARCH | 긴 텍스트 |
   | fldWNE_WORD | 긴 텍스트 |
   | fldWNE_SENSEID | 숫자 |
   | fldWNE_FRAMES | 긴 텍스트 |
   | fldWNE_SOURCES | 긴 텍스트 |
   | fldWNE_INFO | 긴 텍스트 |
   | fldWNE_LANG | 짧은 텍스트 |
   | fldWNE_MORPHINFO | 긴 텍스트 |


  <b>2. tblWN_Relindex</b>

   | 필드 이름 | 데이터 형식 |
   | :----: | :----: |
   | fldWNIR_ONTOLOGY | 짧은 텍스트 |
   | fldWNIR_POS | 짧은 텍스트 |
   | fldWNIR_ELEMENT | 긴 텍스트 |
   | fldWNIR_SENSEID | 숫자 |
   | fldWNIR_RELATION | 긴 텍스트 |
   | fldWNIR_TRGPOS | 짧은 텍스트 |
   | fldWNIR_TRGELEMENT | 긴 텍스트 |
   | fldWNIR_TRGSENSEID | 숫자 |

  <b>3. tblWN_SEIndex</b>

   | 필드 이름 | 데이터 형식 |
   | :----: | :----: |
   | fldWNI_ONTOLOGY | 짧은 텍스트 |
   | fldWNI_POS | 짧은 텍스트 |
   | fldWNI_SOFF | 짧은 텍스트 |
   | fldWNI_WORD | 긴 텍스트 |
   | fldWNI_SENSEID | 숫자 |

  <b>4. tblWN_SSInfo</b>

   | 필드 이름 | 데이터 형식 |
   | :----: | :----: |
   | fldOntology | 짧은 텍스트 |
   | fldPos | 짧은 텍스트 |
   | fldSoff | 짧은 텍스트 |
   | fldLexFn | 짧은 텍스트 |
   | fldXml | 긴 텍스트 |
