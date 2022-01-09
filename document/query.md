## \[tblWN_ELEMENTS\]
  - 어휘 정보
  
    ~~~sql
    SELECT * FROM [tblWN_ELEMENTS] 
    WHERE [fldWNE_ONTOLOGY] = 'KORLEX' AND [fldWNE_POS] = 'n' AND [fldWNE_SEARCH] like '데이터'
    ~~~
    
  - '데이터'는 동음이의어가 없기 때문에 하나의 레코드만이 있다.


## \[tblWN_SEIndex]
  - 어휘를 포함하는 신셋 검색
  
    ~~~sql
    SELECT * FROM [tblWN_SEIndex]
    WHERE [fldWNI_ONTOLOGY] = 'KORLEX' AND [fldWNI_POS] = 'n' AND fldWNI_WORD like '데이터'
    ~~~
  
    | Ontology | POS | SOFF     | WORD  | SENSEID |
    | :------: | :-: | :------: | :---: | :-----: |
    | KORLEX   | n   | 07949563 | 데이터 | 1      |
  
  - "데이터 1"은 신셋 번호가 "07949563"인 신셋에 포함된다.

    ~~~sql
    SELECT * FROM [tblWN_SEIndex]
    WHERE [fldWNI_ONTOLOGY] = 'KORLEX' AND [fldWNI_POS] = 'n' AND fldWNI_SOFF LIKE '07949563'
    ~~~

    | Ontology | POS | SOFF     | WORD  | SENSEID |
    | :------: | :-: | :------: | :---: | :-----: |
    | KORLEX   | n   | 07949563 | 데이터 | 1      |
    | KORLEX   | n   | 07949563 | 자료   | 1      |
    | KORLEX   | n   | 07949563 | 정보   | 2      |
  
  - "데이터 1"과 동일한 신셋(07949563)에 포함된 단어는 "자료 1", "정보 2" 이다. <br>
  즉, 신셋 "07949563"의 데이터는 \[정보2, 자료1, 데이터1]이다.
  
## \[tblWN_SSInfo]
  - 신셋 정보
    
    ~~~sql
    SELECT * FROM [tblWN_SSInfo]
    WHERE [fldOntology] = 'KORLEX' AND [fldPos] = 'n' AND fldSoff like '07949563'
    ~~~
  
    | Ontology | POS | SOFF     | LexFn      | XML      |
    | :------: | :-: | :--:     | :--------: | :------: |
    | KORLEX   | n   | 07949563 | noun.group | 아래 참조 |
  
  
    ~~~xml
    <SYN pos="n" lexfn="noun.group" soff="07949563">
    <domainblock>
    <domain>noun.group</domain>
    </domainblock>
    <WORD senseid="2" seq="1">정보WORD>
    <WORD senseid="1" seq="3">데이터WORD>
    <WORD senseid="1" seq="2">자료WORD>
    <POINTER symbol="child" tsoff="14441576" tpos="n" />
    <POINTER symbol="child" tsoff="07949777" tpos="n" />
    <POINTER symbol="child" tsoff="07950101" tpos="n" />
    <POINTER symbol="child" tsoff="14442942" tpos="n" />
    <POINTER symbol="parent" tsoff="07470940" tpos="n" />
    <POINTER symbol="child" tsoff="07949964" tpos="n" />
    <GLOSS>a collection of facts from which conclusions may be drawn; "statistical data"</GLOSS>
    </SYN>
    ~~~
  
  - 신셋 07949563의 도메인은 "noun.group"이고, 3개의 어휘 [정보2, 자료1, 데이터1]를 포함한다. <br>
  하나의 상위 신셋과 5개의 하위 신셋을 가진다.
  
## \[tblWN_RelIndex]
  - 관계 정보 검색
  
    ~~~sql
    SELECT * FROM [tblWN_RelIndex]
    WHERE [fldWNIR_ONTOLOGY] = 'KORLEX' AND [fldWNIR_POS] = 'n' AND fldWNIR_ELEMENT LIKE '07949563'
    ~~~
  
    ~~~sql
    SELECT * FROM [tblWN_RelIndex]
    WHERE [fldWNIR_ONTOLOGY] = 'KORLEX' AND [fldWNIR_TRGPOS] = 'n' AND fldWNIR_TRGELEMENT LIKE '07949563'
    ~~~
    
    | Ontology | POS | ELEMENT         | SENSEID      | RELATION      | TRGPOS | TRGELEMENT     | TRGSENSEID |
    | :------: | :-: | :---------:     | :----------: | :-----------: | :----: | :------------: | :--------: |
    | KORLEX   | n   | **07949563**    | 0            | parent        | n      | 07470940       | 0          |
    | KORLEX   | n   | **07949563**    | 0            | child         | n      | 14442942       | 0          |
    | KORLEX   | n   | **07949563**    | 0            | child         | n      | 14441576       | 0          |
    | KORLEX   | n   | **07949563**    | 0            | child         | n      | 07950101       | 0          |
    | KORLEX   | n   | **07949563**    | 0            | child         | n      | 07949964       | 0          |
    | KORLEX   | n   | **07949563**    | 0            | child         | n      | 07949777       | 0          |
    | |
    | KORLEX   | n   | 14441576        | 0            | parent        | n      | **07949563**   | 0          |
    | KORLEX   | n   | 14442942        | 0            | parent        | n      | **07949563**   | 0          |
    | KORLEX   | n   | 07949777        | 0            | parent        | n      | **07949563**   | 0          |
    | KORLEX   | n   | 07950101        | 0            | parent        | n      | **07949563**   | 0          |
    | KORLEX   | n   | 07949964        | 0            | parent        | n      | **07949563**   | 0          |
    | KORLEX   | n   | 07470940        | 0            | child         | n      | **07949563**   | 0          |
    
  - 신셋 \[정보2, 자료1, 데이터1]의 상위 신셋은 "07470940"이고, <br>
  하위 신셋은 "14442942", “14441576”, “07950101”, “07949964”, “07949777" 이다.
  - 상위-하위 관계는 상대적이므로 반드시 대칭되는 자료가 있다.
