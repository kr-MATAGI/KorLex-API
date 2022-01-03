# KorLex-Read-API
  "한국어 어휘의미망 KorLex 1.5" 데이터베이스는 아래 그림과 같이 4개의 관계형 테이블로 구성된다.
  
  <img src="https://user-images.githubusercontent.com/30927066/147896306-9666df35-eecd-4453-a606-4411ef5d5fc1.png" width="70%" height="70%">


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
