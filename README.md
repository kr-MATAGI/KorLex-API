# KorLex
  "한국어 어휘의미망 KorLex 1.5" 데이터베이스는 아래 그림과 같이 4개의 관계형 테이블로 구성된다.
  
  <img src="https://user-images.githubusercontent.com/30927066/147896306-9666df35-eecd-4453-a606-4411ef5d5fc1.png" width="70%" height="70%">

  - 품사는 명사(n), 동사(v), 형용사(a), 부사(r)로 나뉜다.

## Table Structure (\[localdb\].mdb)
  <b>1. tblWN_ELEMENTS</b>
  
  - \[tblWN_ELEMENTS] 테이블은 어휘 정보를 나타낸다.
  - key value : fldWNE_ONTOLOGY, fldWNE_POS, fldWNE_WORD, fldWNE_SENSEID
  
   | 필드 이름          | 데이터 형식          | 의 미                   | 길 이   | IS NULL  | Key          | 리스트    |
   | :-------------:  | :---------------: | :--------------------: | :----: | :------: | :----------: | :----:  |
   | fldWNE_ONTOLOGY  | 짧은 텍스트(char)    | 의미망                   | 7      | No       | Primary Key. | 문자열    |
   | fldWNE_POS       | 짧은 텍스트(char)    | 품사                    | 1      | No.      | Primary Key  | 문자      |  
   | fldWNE_SEARCH    | 긴 텍스트(nvarchar) | 검색어형                  | 100    | No       |              | 문자열    |
   | fldWNE_WORD      | 긴 텍스트(nvarchar) | 어형                    | 100     | No       | Primary Key  | 문자열    |
   | fldWNE_SENSEID   | 숫자(tinyint)      | 어의 번호                |         | No       | Primary Key  | 숫자     |
   | fldWNE_FRAMES    | 긴 텍스트(xml)      | 문형 정보                |         |          |              | xml 문서 | 
   | fldWNE_SOURCES   | 긴 텍스트(?).       | ?                      | ?       | ?        | ?            | ?       |
   | fldWNE_INFO      | 긴 텍스트(xml)      | 어의 정보                |         |          |              | xml 문서 |
   | fldWNE_LANG      | 짧은 텍스트(char)   | 언어                    | 2       |          |              | 문자열    |
   | fldWNE_MORPHINFO | 긴 텍스트(?)        | ?                      | ?       | ?        | ?            | ?       | 

  - Field Domain Set
  
  | 필드 이름           | Domain                                          |
  | :---------------: | :---------------------------------------------: |
  | fldWNE_ONTOLOGY   | FRNEWN, JPNWN, KORLEX, PWN3.0, tmponto, WORDNET |
  | fldWNE_POS        | a(adjective), n(noun), r(adverb), v(verb)                                      |
  | fldWNE_SENSEID    | 1 ~ 59 Integer                                  |
  | fldWNE_LANG       | EN, fr, jp, ko                                  |


  <b>2. tblWN_RelIndex</b>
 
  - \[tblWN_RelIndex\]테이블은 \[신셋-신셋\] 관계 혹은 \[어휘-어휘\] 관계를 나타낸다.
  <br>\[신셋-어휘\] 관계는 존재하지 않는다.
  - \[어휘-어휘\] 관계일 때는 fldWNIR_ELEMENT 필드가 어휘를 <br>
  fldWNIR_SENSEID 필드가 어휘 ID를 나타낸다.
  - \[신셋-신셋\] 관계일 때는 fldWNIR_ELEMENT 필드가 신셋번호를 나타내고 <br>
  fldWNIR_SENSEID 필드는 0이 된다.
  - key value : 모든 필드
  <br>

   | 필드 이름            | 데이터 형식          | 의 미                   | 길 이   | IS NULL  | Key          | 리스트    |
   | :----------------: | :---------------: | :--------------------: | :----: | :------: | :----------: | :----:  |
   | fldWNIR_ONTOLOGY   | 짧은 텍스트(char)    | 의미망                   | 7     | No        | Primary Key  | 문자열   |
   | fldWNIR_POS        | 짧은 텍스트(char)    | 품사                    | 1      | No       | Primary Key   | 문자    |
   | fldWNIR_ELEMENT    | 긴 텍스트(nvarchar) | 어형                    | 100    | No       | Primary Key   | 문자열   |
   | fldWNIR_SENSEID    | 숫자(smallint)     | 어의 번호                |        | No       | Primary Key   | 숫자    |
   | fldWNIR_RELATION   | 긴 텍스트(nvarchar) | 의미 관계                | 20     | No       | Primary Key   | 문자열   |
   | fldWNIR_TRGPOS     | 짧은 텍스트(char)    | target 품사             | 1     | No        | Primary Key   | 문자    |
   | fldWNIR_TRGELEMENT | 긴 텍스트(nvarchar) | target 어형             | 100   | No        | Primary Key   | 문자열   |
   | fldWNIR_TRGSENSEID | 숫자(smallint)     | target 어의 번호         |       | No        | Primary Key   | 숫자    |
   
  - Field Domain Set

  | 필드 이름            | Domain                                          |
  | :---------------:  | :---------------------------------------------: |
  | fldWNIR_ONTOLOGY   | FRNEWN, JPNWN, KORLEX, PWN3.0, WORDNET          |
  | fldWNIR_POS        | a, n, r, v                                      |
  | fldWNIR_SENSEID    | 0 ~ 57 Integer                                  |
  | fldWNIR_TRGPOS     | a(adjectivce), n(noun), r(adverb), v(verb)                                      |
  | fldWNIR_TRGSENSEID | 0 ~ 57 Integer                                  |
   
  + 관계 심벌
    - 아래 테이블의 \[fldWNIR_RELATION\] 필드는 KorLex의 의미 관계를 나타내는 심벌로서<br>
    다음 표와 같이 정의된다. 
    - 기본적으로 영어 워드넷 PWN의 심벌과 동일하며 예외적으로 상위어와 하위어는 각각 "parent"와 "child"를 사용한다.
    - 실제 테이블 자료에는 아래 표에 없는 "@", "~" 등이 있지만 영어 워드넷과의 호환성을 위해 남아있는 자료이므로<br>
    "parent"와 "child"를 사용하는 것이 정확하다.
    <br>
    
    + 명사

    <img src="https://user-images.githubusercontent.com/30927066/147902881-00c2f04e-6736-473e-924c-6edc0e9b4152.png" width="50%" height="60%">
    
    + 동사
    
    <img src="https://user-images.githubusercontent.com/30927066/147902950-f68f7eb8-5685-4e26-a482-d01ade6a51b2.png" width="50%" height="60%">
    
    + 형용사

    <img src="https://user-images.githubusercontent.com/30927066/147902979-94d17f4f-9a6a-490a-9719-6ee1e7389b97.png" width="50%" height="60%">

    + 부사
    
    <img src="https://user-images.githubusercontent.com/30927066/147903001-6de4c1a4-4781-4736-9e4a-d5556970606e.png" width="50%" height="60%">

  <b>3. tblWN_SEIndex</b>

  - \[tblWN_SEIndex\] 테이블은 신셋과 어휘의 연결 정보를 나타낸다.
  - 즉, 신셋이 어떤 어휘를 포함하고 있는지, 또는 반대로 어휘가 어느 신셋에 포함되는지를 표현한다.
  <br> 이 정보는 \[tblWN_SSInfo\] 테이블의 \[fldXml\] 필드에도 있지만(WORD 요소),<br>검색이 힘들기 때문에 검색용 인덱스 테이블로 \[tblWN_SEIndex\]를 사용한다.
  - key value : 모든 필드

   | 필드 이름          | 데이터 형식           | 의 미                   | 길 이   | IS NULL  | Key          | 리스트    |
   | :--------------: | :---------------:  | :--------------------: | :----: | :------: | :----------: | :----:  |
   | fldWNI_ONTOLOGY  | 짧은 텍스트(char)     | 의미망	                 | 7     | No        | Primary Key  | 문자열   |
   | fldWNI_POS       | 짧은 텍스트(char)     | 품사                     | 1     | No       | Primary Key  | 문자     |
   | fldWNI_SOFF      | 짧은 텍스트(navrchar) | 신셋 고유번호              | 100   | No       | Primary Key  | 문자열    |
   | fldWNI_WORD      | 긴 텍스트(navrchar)  | 어형                     | 100   | No       | Primary Key  | 문자열    |
   | fldWNI_SENSEID   | 숫자(tinyint)       | 어의 번호                 |       | No       | Primary Key  | 숫자     |

  - Field Domain Set

  | 필드 이름            | Domain                                           |
  | :---------------:  | :----------------------------------------------: |
  | fldWNI_ONTOLOGY    | FRNEWN, JPNWN, KORLEX, PWN3.0, tmponto, WORDNET  |
  | fldWNI_POS         | a(adjective), n(noun), r(adverb), v(verb)                                       |
  | fldWNI_SENSEID     | 1 ~ 59 Integer                                   |

  <b>4. tblWN_SSInfo</b>
  
  - \[tblWN_SSInfo\] 테이블은 신셋(synonym set: 동의어 집합)에 대한 정보를 나타낸댜. <br> 신셋은 각 품사별로 8자리의 고유번호를 가진다.
  - key value : fldOntology, fldPos, fldSoff

   | 필드 이름     | 데이터 형식       | 의 미                   | 길 이   | IS NULL  | Key          | 리스트    |
   | :---------: | :------------: | :--------------------: | :----: | :------: | :----------: | :----:  |
   | fldOntology | 짧은 텍스트(char) | 의미망                   | 7     |  No       | Primary Key  | 문자열   |
   | fldPos      | 짧은 텍스트(char) | 품사                    | 1      | No       | Primary Key  | 문자     |
   | fldSoff     | 짧은 텍스트(char) | 신셋 고유번호             | 8      | No       | Primary Key   | 문자열   |
   | fldLexFn    | 짧은 텍스트(char) | Lexical life <br> 도메인 | 20    | No       |               | 문자열    |
   | fldXml      | 긴 텍스트(xml)   | 신셋 정보                 |       |          |               | xml 문서 |

  - Field Domain Set

  | 필드 이름            | Domain                                           |
  | :---------------:  | :----------------------------------------------- |
  | fldONTOLOGY        | FRNEWN, JPNWN, KORLEX, PWN3.0, tmponto, WORDNET  |
  | fldPOS             | a(adjective), n(noun), r(adverb), v(verb)                                       |
  | fldLexFn           | adj, adj.{all, pert, ppl}                        |
  | fldLexFn           | adv.all                                          |
  | fldLexFn           | noun, noun.{act, animal, artifact, attribute, body, cognition, communication, event, feeling, food, group, hetercompound, location, motive, object, person, phenomenon, plant, possession, process, quantity, relation, shape, state, substance, time, Tops|
  | fldLexFn           | verb.{body, change, cognition, communication, competition, consumption, contact, creation, emotion, motion, preception, possession, social, stative, weather} |
  
  - 다음은 fldXml이 나타내는 요소와 의미 설명이다.

   | 요소명        | 설명                                                                                                |
   | :---------: | :------------------------------------------------------------------------------------------------- |
   | SYN         | 하나의 의미(substance)를 의미한다. <br> 내부의 다수의 pointer 정보와 어휘정보, 도메인 정보, 설명문 정보를 포함할 수 있다. |
   | WORD        | 의미를 표식(시?)하는 어휘정보다. 각각 sense의 번호를 포함한다.                                                  |
   | POINTER     | 타의미와 관계를 나타낸다. <br> 하나 이상이 포함될 수 있으며, 특정한 심벌과 대상 의미의 번호, 품사 정보를 포함한다.          |
   | GLOSS       | 어휘의 의미를 설명할 수 있는 일반적인 내용을 담는다.                                                           |
   | domainblock | 도메인 정보를 담는다.                                                                                   |

  e.g. 동사 01064957 {지다1, 패배하다1, 패하다1}의 신셋 정보

 | 신셋 정보                                                                  | 설명                                          |
 | :----------------------------------------------------------------------- | :------------------------------------------- |
 | \<SYN pos="v" lexfn="verb.competition" soff="01064957" descendent="0">    | PWN 품사, 의미분류, 신셋번호, 하위노드 유무           |
 |  \<POINTER symbol="Topic-Domain-of-Synset" tsoff="00407449" tpos="n"/>    | PWN의 신셋의 의미관계: 영역(전문분야)                |
 |  \<POINTER symbol="parent" toff="01064559" tpos="v"/>                     | PWN의 신셋의 의미관계: 상위노드                     |
 |  \<GLOSS>lose (a game): "The Giants dropped 11 of their first 13"</GLOSS> | PWN의 정의문                                    |
 |  \<DOMAIN>verb.competition</DOMAIN>                                       | KorLex 의미분류                                 |
 |  \<WORD senseid="1" seq="0">지다</WORD>                                    | KorLex 신셋을 구성하는 어의 1: '지다1'              |
 |  \<WORD senseid="1" seq="1">패배하다</WORD>                                 | KorLex 신셋을 구성하는 어의 2: '패배하다1'           |
 |  \<WORD senseid="1" seq="2">패하다</WORD>                                  | KorLex 신셋을 구성하는 어의 3: '패하다1'             |
 |  \<POINTER symbol="parent" tsoff="01064559" tpos="v"/>                    | KorLex 신셋의 의미관계: 상위노드                    |
 |  \<POINTER symbol="child" tsoff="02691569" tpos="v"/>                     | KorLex 신셋의 의미관계: 하위노드                    |
 |  \<POINTER symbol="child" tsoff="02692052" tpos="v"/>                     | KorLex 신셋의 의미관계: 하위노드                    |
 | \</SYN>                                                                   |                                               |
  
