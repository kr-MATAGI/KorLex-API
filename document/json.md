# Json Result Format
  - 아래에서는 make_korlex_result_json() 함수로 return 되는 JSON schema에 대해 설명한다.

## KorLex Web
  - KorLext Web에서 "사과"를 검색하면 아래와 같은 화면을 출력한다.
  - 아래는 word="사과", senseId="1" 의 출력
 
  ![image](https://user-images.githubusercontent.com/30927066/148749084-10f5dce2-1a18-4ebb-905c-d7690707c0f8.png)
  
  - 아래는 word="사과", senseId="2" 의 출력이다.
  
  ![image](https://user-images.githubusercontent.com/30927066/148749312-748cb054-9285-49df-a19c-f42556962133.png)

  **위 두 결과에 대한 JSON은 따로 생성됨을 명시한다.**
  
## Json Format
### Root Format
  ~~~json
    {
      "korlex": string (defulat: korlex),
      "search_word": string (Not NULL)
      "search_senseid": string (Not NULL, integer type)
      "restuls": array
    }
  ~~~
  
### Results Inner Format
  - 웹 출력과 동일하게 "KorLex" 노드를 제외한 첫 노드부터 데이터가 입력되어있다.
  ~~~json
    {
      "word_set": array,
      "soff": string (integer type)
    }
  ~~~

### Wordset Inner Format
  ~~~json
  {
    "word": string
    "senseid": string (integer type)
  }
  ~~~
