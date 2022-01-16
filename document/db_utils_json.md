# DB Utils의 JSON Format
  - *.mdb 파일을 이용해 ontology 별 json을 생성하였을 시, 아래와 같은 Format을 가진다.

## Word2Synset, Synset2Word (Dictionary)
  ### Word2Synset Dictionary
  
  ~~~
      word: key (string),
      soff(synset) : value (integer)
  ~~~
  
  ### Synset2Word Dictionary
  
  ~~~
    soff(synset): key (integer),
    word: value (string)
  ~~~
   
   
## ssinfo and relation info(all info) json
   ### all_info_dict
   
  ~~~python
  {
    "pos": str,
    "lexFn": str,
    "synset_info": dict(),
    "relation_info: array()
  }
  ~~~
    
  ### synset_info
    
  ~~~python
  {
    "syn": {
      "pos": str,
      "lexfn": "",
      "soff": int,
      "descendent": int
    },
    "gloss": str,
    "domain": str,
    "word": array(),
    "pointer": array()
  }
  ~~~
  
  - word

  ~~~python
  {
    "senseid": int,
    "seq": int,
    "text": str
  }
  ~~~
  
  - pointer
  
  ~~~python
  {
    "symbol": str,
    "tsoff": int,
    "tpos": str
  }
  ~~~
  
  ### relation info
  
  ~~~python
  {
    "ontology": str,
    "pos": str,
    "elem": int,
    "senseid": int,
    "relation": str,
    "trg": {
      "pos: str,
      "elem: int,
      "senseid": int
    }
  }  
  ~~~
