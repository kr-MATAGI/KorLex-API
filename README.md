# KorLex-Read-API
  "한국어 어휘의미망 KorLex 1.5" 데이터베이스는 아래 그림과 같이 4개의 관계형 테이블로 구성된다.
  
  <img src="https://user-images.githubusercontent.com/30927066/147896306-9666df35-eecd-4453-a606-4411ef5d5fc1.png" width="70%" height="70%">

  - 품사는 명사(n), 동사(v), 형용사(a), 부사(r)로 나뉜다.

## Table Structure (\[localdb\].mdb)
  <b>1. tblWN_ELEMENTS</b>
   
   | 필드 이름     | 데이터 형식       | 의 미                   | 길 이   | IS NULL  | Key          | 리스트    |
   | :---------: | :------------: | :--------------------: | :----: | :------: | :----------: | :----:  |
   | fldWNE_ONTOLOGY | 짧은 텍스트(char) |
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

   | 필드 이름     | 데이터 형식       | 의 미                   | 길 이   | IS NULL  | Key          | 리스트    |
   | :---------: | :------------: | :--------------------: | :----: | :------: | :----------: | :----:  |
   | fldOntology | 짧은 텍스트(char) | 의미망                   | 7     |  NO       | Primary Key  | 문자열   |
   | fldPos      | 짧은 텍스트(char) | 품사                    | 1      | NO       | Primary Key  | 문자     |
   | fldSoff     | 짧은 텍스트(char) | 신셋 고유번호             | 8      | NO       | Primary Key   | 문자열   |
   | fldLexFn    | 짧은 텍스트(char) | Lexical life <br> 도메인 | 20    | NO       |               | 문자열    |
   | fldXml      | 긴 텍스트(xml)   | 신셋 정보                 |       |          |               | xml 문서 |

  - \[tblWN_SSInfo\] 테이블은 신셋(synonym set: 동의어 집합)에 대한 정보를 나타낸댜. <br> 신셋은 각 품사별로 8자리의 고유번호를 가진다.
  - key value : fldOntology, fldPos, fldSoff
  - 다음은 fldXml이 나타내는 요소와 의미 설명이다.

   | 요소명        | 설명                                                                                                |
   | :---------: | :------------------------------------------------------------------------------------------------- |
   | SYN         | 하나의 의미(substance)를 의미한다. <br> 내부의 다수의 pointer 정보와 어휘정보, 도메인 정보, 설명문 정보를 포함할 수 있다. |
   | WORD        | 의미를 표식(시?)하는 어휘정보다. 각각 sense의 번호를 포함한다.                                                  |
   | POINTER     | 타의미와 관계를 나타낸다. <br> 하나 이상이 포함될 수 있으며, 특정한 심벌과 대상 의미의 번호, 품사 정보를 포함한다.          |
   | GLOSS       | 어휘의 의미를 설명할 수 있는 일반적인 내용을 담는다.                                                           |
   | domainblock | 도메인 정보를 담는다.                                                                                   |
