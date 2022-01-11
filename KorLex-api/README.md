# KorLex API
  - 기존의 KorLex 웹에서 출력되는 아래의 정보를 Python 에서 Local DB를 이용해 KorLex를 사용할 수 있도록 함.
  
  ![image](https://user-images.githubusercontent.com/30927066/148867056-a93b3536-89af-4354-944b-94022e9272f4.png)

  
## 사용하기 전에...
  - 본 KorLex-api는 Windows 환경에서 사용하기를 권장.
  - [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920) 링크에서 드라이버를 다운로드하여 설치.
  - python을 이용해서인지 웹 보다 속도면에서 느림.
  
## Method
  1. _local_db_connect(mdb_path:str)
    - private
    - 
  2. search_synset_info(conn:pyodbc.Connection, mdb_path:str, soff:str, pos:str)
    - public

  3. search_sibling_nodes(conn:pyodbc.Connection, mdb_path:str, word:str)
    - public

  5. search_relation_index_info(conn:pyodbc.Connection, mdb_path:str, soff:str)
    - public

  7. search_soff_children(conn:pyodbc.Connection, mdb_path:str, soff:str)
    - public
  
  ### For Users
  1. make_korlex_tree_resource(word:str, mdb_path:str)
  2. make_korlex_result_json(json_rsrc_list:list)
