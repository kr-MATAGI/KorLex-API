# KorLex API
  - 기존의 KorLex 웹에서 출력되는 아래의 정보를 Python 에서 Local DB를 이용해 KorLex를 사용할 수 있도록 함.
  
  ![image](https://user-images.githubusercontent.com/30927066/148867056-a93b3536-89af-4354-944b-94022e9272f4.png)

  
## 사용하기 전에...
  - 본 KorLex-api는 Windows 환경에서 사용하기를 권장.
  - [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920) 링크에서 드라이버를 다운로드하여 설치.
  - python을 이용해서인지 웹 보다 속도면에서 느림.
  

## Method
  **1. def _local_db_connect(mdb_path:str)**

  ~~~python
    def _local_db_connect(mdb_path:str) -> conn:pyodbc.Connection, cursor:pyodbc.Cursor
  ~~~
    
  - private
  - 내부적으로 mdb_path에 해당하는 KorLex Database와 연결하기 위해 사용.
    
  **2. def search_synset_info(conn:pyodbc.Connection, mdb_path:str, soff:str, pos:str)**
  
  ~~~python
    def search_synset_info(conn:pyodbc.Connection, mdb_path:str, soff:str, pos:str) -> korlexDef.SynsetData
  ~~~
    
  - public
  - \[tblWN_SSInfo] 테이블에서 fldXml 필드를 통해 동음이의어, parent, child 단어 정보를 얻는다.
  - 단독으로 이 함수를 사용할 경우, conn의 매개변수를 사용해야 mdb와 연결이 가능하다.

  **3. search_sibling_nodes(conn:pyodbc.Connection, mdb_path:str, word:str)**

  ~~~python
    def search_sibling_nodes(conn:pyodbc.Connection, mdb_path:str, word:str) -> siblingNodeList:list
  ~~~
    
  - public
  - \[tblWN_SEIndex] 테이블에서 아래와 같이 KorLex Web에서 사과를 검색했을 때, 동음이의어(?)를 찾아서 반환한다.

  ![image](https://user-images.githubusercontent.com/30927066/148869392-5dc8fa12-8f94-47c2-8b44-2a7c1565b597.png) 

  - 단독으로 이 함수를 사용할 경우, conn의 매개변수를 사용해야 mdb와 연결이 가능하다.

  **4. search_relation_index_info(conn:pyodbc.Connection, mdb_path:str, soff:str)**

  ~~~python
    def search_relation_index_info(conn:pyodbc.Connection, mdb_path:str, soff:str) -> ret_element:(None|list)
  ~~~
    
  - public
  - \[tblWN_RelIndex] 테이블에서 target이 되는 단어의 부모를 찾는다. (즉, fldWNIR_ELEMENT 필드에서 "child"인 것을 찾는다)
  - 단독으로 이 함수를 사용할 경우, conn의 매개변수를 사용해야 mdb와 연결이 가능하다.

  **5. search_soff_children(conn:pyodbc.Connection, mdb_path:str, soff:str)**
    
  ~~~python
    def search_soff_children(conn:pyodbc.Connection, mdb_path:str, soff:str) -> ret_child_list:list
  ~~~
    
  - public
  - \[tblWN_SSInfo] 테이블에서 모든 "child"를 찾는다.
  - 단독으로 이 함수를 사용할 경우, conn의 매개변수를 사용해야 mdb와 연결이 가능하다.
    
  ### For Users
  **1. make_korlex_tree_resource(word:str, mdb_path:str)**
    
  ~~~python
    def make_korlex_tree_resource(word:str, mdb_path:str) -> ret_json_rsrc_list:list
  ~~~

  - public
  - KorLex Web과 같은 결과를 얻기 위해 사용하는 함수.
  - 검색된 단어의 동음이의어 마다의 결과를 list에 넣어 반환한다.
  - **korlexDef.KorLexJson** 구조체 참조.
    
  **2. def make_korlex_result_json(json_rsrc_list:list)**
    
  ~~~python
    def make_korlex_result_json(json_rsrc_list:list) -> ret_json.decode():str
  ~~~

  - public
  - <code>make_korlex_tree_resource()</code> 로 반환된 구조체 객체를 json string으로 만들어준다.
  - documnet/json.md 참조
