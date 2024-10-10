# Python Map, Reduce 구현

## Programming Model: MapReduce

### Warm-up task:

- **목적**: 큰 텍스트 문서에서 각 단어가 몇 번 나타나는지 세기
    - 이는 단순 텍스트가 아니라 웹사이트의 방문자 수와 같은 다른 데이터일 수도 있음
- 파일에서 고유한 단어가 등장하는 빈도를 카운트하는 작업

### Sample Application:

- **적용 예시**: 웹 서버 로그 분석을 통해 인기 있는 URL 찾기

### Word Count Example:

- **Count occurrences of words**:
    - `words(doc.txt) | sort | uniq -c`
        - `words` 함수는 파일을 읽어 각 단어를 한 줄씩 출력
        - 그 후 단어 목록을 알파벳순으로 정렬하고, 중복된 단어를 제거하며 등장 횟수를 계산

### MapReduce의 핵심:

- 이 프로세스는 **MapReduce**의 본질그자체를 나타냄:
    - 가장 큰 **장점**은 자연스럽게 병렬화가 가능하다는 것
    - 즉, 각 단계가 **독립적으로 실행**되기 때문에 대용량 데이터를 병렬로 처리할 수 있음

---

1. **`words(doc.txt)`**: `doc.txt` 파일에서 각 단어를 한 줄씩 출력
2. **`sort`**: 첫 번째 명령어의 출력(단어 목록)을 입력으로 받아 단어를 알파벳순으로 정렬
3. **`uniq -c`**: 정렬된 결과를 받아 중복된 단어를 제거하고, 각 단어의 빈도를 계산하여 출력

따라서 **`|` (파이프)**는 각 명령어의 출력을 다음 명령어의 입력으로 연결해 작업을 연속적으로 처리하게 만듦. 이 과정은 서로 **Dependency(의존성)**가 없기 때문에 대용량 데이터를 **병렬 처리**할 수 있다는 점에서 매우 유용함.

[hadoop.txt](https://prod-files-secure.s3.us-west-2.amazonaws.com/fb0c0b3a-b027-4183-8d68-2a94adb0c0c6/dad88009-f40f-4493-9a17-d4f6d6579d56/hadoop.txt)

# Mapper.py

```python
#!/usr/bin/env python
"""mapper.py"""
import sys

for line in sys.stdin:
    # 한줄씩 읽어온 문자열의 개행문자와 공백 제거
    line = line.strip()
    # ' '을 기준으로 단어를 분할함
    words = line.split()
    # 각 단어(Key)마다 1이라는 값(Value)을 할당하여 등장 빈도를 나타냄.
    for word in words:
        print ('%s\t%s' % (word, 1))
```

```python
echo " Deer Bear River Car Car River Deer Car Bear" | python3 mapper.py
```

```python
# 출력
Deer    1
Bear    1
River   1
Car     1
Car     1
River   1
Deer    1
Car     1
Bear    1
```

1. **`sort`**: 첫 번째 명령어의 출력(단어 목록)을 입력으로 받아 단어를 알파벳순으로 정렬

결과:

```python
Bear    1
Bear    1
Car     1
Car     1
Car     1
Deer    1
Deer    1
River   1
River   1
```

# Reducer.py

```python
#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys
'''
Bear    1
Bear    1
Car     1
Car     1
Car     1
Deer    1
Deer    1
River   1
River   1
'''
# mapper 가 input을 <key,value>형태로 반환 
# sort -k1,1 , sort함수로 각 첫번 째 열의 단어를 key로 수를 value로 정렬한 후 reducer에 전달
current_word = None
current_count = 0
word = None

for line in sys.stdin:
    
    line = line.strip()
    # 각 단어(Key)마다 1이라는 값(Value)을 할당하여 등장 빈도를 나타냄.
    # mapper 로 부터 받은 <key,value> 튜플을 parsing
    word, count = line.split('\t',1)
    
    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # 만약 숫자로 변환할 수 없으면 해당 line을 무시하고 진행
        continue

    # sort 함수에 의해 이미 key를 기준으로 텍스트가 정렬된 상태로 reducer에 전달
    # 따라서 리듀서는 현재 단어를 기준으로 카운팅해서 반환하면 됨.
    if current_word == word:
        # 만약 current_word가 이미 존재한다면
        current_count += count # <current_count+1>
    else:
        if current_word:
            print('%s\t%s' % (current_word, current_count))
        
        current_count = count
        current_word = word

# 마지막 단어가 출력되기 전에 반복문이 종료될 수 있으므로 마지막 단어를 출력함
if current_word == word:
    print('%s\t%s' % (current_word, current_count))
```

```python
echo " Deer Bear River Car Car River Deer Car Bear" | python3 mapper.py | sort -k1,1 
| python3 reducer.py
```

결과:

```python
Bear    2
Car     3
Deer    2
River   2
```

## MapReduce: Overall Procedures

1. **Sequentially read a lot of data**
    - 데이터를 순차적으로 읽어들임
2. **Map**:
    - 처리하고자 하는<관심있는> 데이터를 추출함
3. **Group by key**:
    - 데이터를 키로 그룹화하고 정렬 및 셔플을 수행함
4. **Reduce**:
    - 데이터를 집계, 요약, 필터 또는 변환함
5. **Write the result**:
    - 결과를 기록함
