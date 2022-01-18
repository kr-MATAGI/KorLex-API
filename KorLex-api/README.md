# KorLex API
  - 기존의 KorLex 웹에서 출력되는 아래의 정보를 Python 에서 Local DB를 이용해 KorLex를 사용할 수 있도록 함.
  
  ![image](https://user-images.githubusercontent.com/30927066/148867056-a93b3536-89af-4354-944b-94022e9272f4.png)

  
## 사용하기 전에...
  - 본 api는 korlex의 \*.mdb파일을 기반으로 \*.pkl을 파일을 만들어 검색에 사용한다.
  - 만약, \*.mdb파일을 직접 사용하고 싶다면 아래의 드라이버를 설치해야한다.
  - [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920) 링크에서 드라이버를 다운로드하여 설치.

## Enum Class
  - Query문은 제외하고 업로드
  
  **1. ONTOLOGY**
  ~~~python
    class ONTOLOGY(Enum):
      KORLEX = "KORLEX"
      WORDNET = "WORDNET"
      FRNEWN = "FRNEWN"
      JPNWN = "JPNWN"
      PWN3 = "PWN3.0"
  ~~~

## Data Structure
  - krx_def.py 참조
  
  **1. Target**
  
  - api를 통해 검색하고자 하는 정보를 결과에서 확인할 수 있도록 한다. (즉, 사용자가 입력한 word 정보)
  
  ~~~java
    @dataclass
    class Target:
      ontology:str
      word:str
      sense_id:str
      pos:str
      soff:str
  ~~~
  
  **2. SS_Node**
  
  - synset 관계를 표현하기 위한 구조체, synset_list에는 같은 soff를 가지는 word들이 들어간다.
  
  ~~~java
    @dataclass
    class SS_Node:
      synset_list: list()
      soff: int
      pos:str
  ~~~
  
  **3. KorLexresult**
  
  - 동음이의어 하나당 만들어지는 결과에 대한 구조체
  - results, siblings에는 SS_Node를 요소로 가진다.
  
  ~~~java
    @dataclass
    class KorLexResult:
      target: Target()
      results: list()
      siblings: list()
  ~~~  

## Method
  - krx_api_의 사용순서는 아래와 같이 사용한다.
    
    1) KorLexAPI(ssInfo_path="", seIdx_path="", reIdx="")를 통해 \*.pkl의 경로를 설정하며 인스턴스를 생성한다.
    2) KorLexAPI.load_synset_data를 통해 (1)에서 설정한 경로의 \*.pkl을 메모리에 적재한다.
    3) KorLexAPI.search_word(word="", ontology="")를 통해서 검색을 하고 결과를 반환받는다.
