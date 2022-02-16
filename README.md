# branching-entropy-with-pos-tagger

Branching Entropy를 형태소 분석과 함께 신조어 탐색에 써볼 수 없을까 생각하며 테스트해본 레포지토리입니다.
[나무위키 코퍼스](https://jeongukjae.github.io/tfds-korean/datasets/namuwiki_corpus.html)를 기준으로 형태소 분절 후 Branching Entropy를 계산하였습니다.

설명 블로그 글: <https://jeongukjae.github.io/posts/pos-tagger-branching-entropy/>

## 방법

1. [nori-clone](https://github.com/jeongukjae/nori-clone)을 활용하여 대량의 약 200만 문장을 분절
2. 분절된 형태소 기준으로 branching entropy를 계산
3. entropy가 높은 순대로 csv로 덤프

특정 형태소가 포함되거나, 특정 형태소로 끝나는 경우는 분석 결과에서 제외했습니다.

## 결과

* [left -> right entropy 계산 결과](./entropy-table-left.csv)
* [right -> left entropy 계산 결과](./entropy-table-right.csv)

## 실행

```
./download.sh
python extract.py
```

## 참고

* <https://lovit.github.io/nlp/2018/04/09/branching_entropy_accessor_variety/>
* <https://aclanthology.org/P06-2056/>
