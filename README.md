# branching-entropy-with-pos-tagger

Branching Entropy를 형태소 분석과 함께 신조어 탐색에 써볼 수 없을까 생각하며 테스트해본 레포지토리입니다.
[나무위키 코퍼스](https://jeongukjae.github.io/tfds-korean/datasets/namuwiki_corpus.html)를 기준으로 형태소 분절 후 Branching Entropy를 계산하였습니다.

## 방법

1. [nori-clone](https://github.com/jeongukjae/nori-clone)을 활용하여 대량의 약 200만 문장을 분절
2. 분절된 형태소 기준으로 branching entropy를 계산
3. entropy가 높은 순대로 csv로 덤프

특정 형태소가 포함되거나, 특정 형태소로 끝나는 경우는 분석 결과에서 제외했습니다.

## 결과

* [left -> right entropy 계산 결과](./entropy-table-left.csv)
* [right -> left entropy 계산 결과](./entropy-table-right.csv)

## 참고

* <https://lovit.github.io/nlp/2018/04/09/branching_entropy_accessor_variety/>
* <https://www.researchgate.net/profile/Zhihui-Jin/publication/220873812_Unsupervised_Segmentation_of_Chinese_Text_by_Use_of_Branching_Entropy/links/561db42808aecade1acb403e/Unsupervised-Segmentation-of-Chinese-Text-by-Use-of-Branching-Entropy.pdf>
