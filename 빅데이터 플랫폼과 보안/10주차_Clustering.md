
# The BFR Algorithm
### Extension of k-means to large data

## BFR 알고리즘

### 개요
- BFR(Bradley-Fayyad-Reina)은 k-평균의 변형 알고리즘이다.
- **매우 큰 데이터셋**을 처리하도록 설계되었다. -> k-mean의 단점

### 클러스터 형태에 대한 가정
- 클러스터는 유클리드 공간에서 중심을 기준으로 `정규 분포`를 따른다.
- 클러스터의 평균과 표준 편차는 각 차원마다 다를 수 있다.
- 클러스터는 축에 정렬된 타원형이다.
- 클러스터의 축은 공간의 축과 정렬되어야 한다.
- 그 이유는 x,y 축을 기준으로 데이터들의 표준편차를 기준으로 클러스터링 하기 때문에
![image](https://github.com/user-attachments/assets/2c3d5243-9b9b-4819-a66b-c9153bf2ce1d)

### 클러스터 요약의 효율성
- 클러스터를 요약하는 효율적인 방법을 제공한다.
- 메모리 요구량이 O(데이터) 대신 O(클러스터)가 되도록 한다.


## Three Classes of Points

데이터 포인트들을 읽어와서 3가지 집합으로 분류한다.
1. Discard set (DS):
   - 할당된 점(포인트)들이 센트로이드에 충분히 가까운 경우 
   - 이 점들을 이용해 정보를 업데이트한 후 점들을 버린다.
2. Compressed set (CS):
   - 현재 센트로이드에 가깝지는 않지만 할당된 점 끼리는 작은 클러스터를 만들 수 있을 정도로 가까운 경우
   - 이 점들을 이용해 정보를 업데이트한 후 점들을 버린다.
3. Retained set (RS): 
   -  센트로이드와 가깝지도 않고 서로 충분히 가까워 작은 클러스터를 만들 수 없는 이도저도 아닌 점들은 큰 메모리를 잡아먹지 않기 때문에 유지함
  
![image](https://github.com/user-attachments/assets/161385ea-1304-4628-983d-458baf6eba28)

각 클러스터에 대해, Discard set (DS)와 Compressed set (CS)는 다음과 같이 요약된다:
- \( N \): 점의 수
- 길이 \( d \)의 벡터 \( \text{SUM} \) (d는 차원의 수): 각 차원에서 모든 점의 성분 합
  - \( \text{SUM}_i \): 벡터 SUM의 i번째 차원의 좌표 합
- 길이 \( d \)의 벡터 \( \text{SUMSQ} \): 각 차원에서 모든 점의 성분 제곱 합
  - \( \text{SUMSQ}_i \): 벡터 SUMSQ의 i번째 차원의 좌표 제곱 합

목표: 점 집합을 (1) 점의 수, (2) 중심점(centroid), (3) 각 차원의 표준 편차(STDEV)로 표현한다.
- \( 2d + 1 \) 값이 이러한 통계를 제공한다 (d = 차원의 수).
- \( N \): 점의 수.

- 각 차원의 `평균` = \( \frac{\text{SUM}_i}{N} \) (centroid)
  - 즉, 센트로이드를 계산할 필요 없이 \( \frac{\text{SUM}_i}{N} \)으로 얻을 수 있다.
  - \( \text{SUM}_i \): SUM의 i번째 성분.
- 클러스터의 discard set의 i번째 차원의 `분산` = \( \frac{\text{SUMSQ}_i}{N} - \left( \frac{\text{SUM}_i}{N} \right)^2 \)
  - 참고: \( \text{Var}(X) = \mathbb{E}[(X - \mathbb{E}[X])^2] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 \)
  - 분산의 제곱근 = 표준 편차(STDEV).

Q: 왜 중심점과 표준 편차를 직접 저장하는 대신 이 표현을 사용하는가?
    -> 각 점이 할당될때 마다 센트로이드와 분산을 계산하지 않기 위해서 즉, 오버헤드를 방지하기 위해
## Processing the “Memory-Load” of points (1)

1. 클러스터 중심에 "충분히 가까운" 점들을 찾아 해당 클러스터와 DS에 추가한 후, 이 점들을 버린다.
   - 새로운 점들을 반영하여 클러스터의 통계량을 조정한다: \( N_s \), \( \text{SUM}_s \), \( \text{SUMSQ}_s \)

2. 어떤 중심에도 충분히 가깝지 않은 점들에 대해서는, 메인 메모리 클러스터링 알고리즘을 사용하여 남은 점들과 기존 RS를 클러스터링한다.
   - 클러스터를 요약하여 CS에 추가한다.
   - 외곽 점들(즉, 단일 클러스터)은 RS가 된다.

## Processing the “Memory-Load” of points (2)

3. 새로운 미니 클러스터들을 기존 CS 와 서로 병합하는 것을 고려한다.

4. 클러스터나 미니 클러스터에 할당된 점들(즉, RS에 속하지 않은 점들)은 보조 메모리에 기록한다.

5. 만약 이것이 마지막 입력 데이터 청크라면, CS와 RS에 대해 다음과 같은 처리를 해야 한다.
   - 이들을 이상치로 간주하여 전혀 클러스터링하지 않는다.
   - RS의 각 점을 가장 가까운 중심 클러스터에 할당한다.
   - 각 미니 클러스터를 가장 가까운 중심 클러스터와 결합한다.
  
## 고려해야할 부분
Q1) 점이 클러스터에 "충분히 가까운지"를 어떻게 결정하는가?
- 점과 클러스터 중심 간의 거리(예: 유클리드 거리 혹은 측도)가 미리 정의된 `임계값` 이하인 경우, 점을 해당 클러스터에 추가한다.

Q2) 두 개의 압축 집합(CS)<미니 클러스터>을 하나로 결합할 가치가 있는지 어떻게 결정하는가?
- 두 압축 집합의 중심 간의 거리와 각 집합의 분산을 고려하여, 미리 정의된 임계값 이하인 경우 두 집합을 결합한다.

### Q1
새로운 점을 클러스터에 넣고 버릴지 결정하는 방법이 필요하다.
- `BFR`은 두 가지 방법을 제안한다:
  - 현재 가장 가까운 중심에 속할 가능성이 높은 경우.
  - `마할라노비스` 거리가 임계값보다 작은 경우.
  - ![image](https://github.com/user-attachments/assets/f7e7b3be-42d5-41ca-b601-810978287707)

### 마할라노비스 거리 (Mahalanobis Distance)
#### 정규화된 유클리드 거리 (Normalized Euclidean Distance) from centroid
- 클러스터의 각 차원에서 표준 편차(STDEV)로 정규화된, 점과 클러스터 중심 간의 거리.

#### 점 (x1, …, xd)와 중심점 (c1, …, cd)에 대해
1. 각 차원에서 유클리디안 거리를 정규화: \( y_i = \frac{x_i - c_i}{\sigma_i} \)
2. \( y_i \)의 제곱 합을 구한다.
3. 제곱근을 구한다.
\[ d(x, c) = \sqrt{\sum_{i=1}^{d} \left( \frac{x_i - c_i}{\sigma_i} \right)^2} \]
- \( \sigma_i \): i번째 차원에서 클러스터 내 점들의 표준 편차.
  
즉, 평균이 0인 점에서 각 데이터 포인트와 센트로이드 사이의 유클리디안 거리를 계산한 값이 표준편차를 기준으로 데이터 할당의 임계값을 결정함

점 \( p \)를 클러스터에 할당하기 위해:
- \( p \)와 각 클러스터 중심 간의 마할라노비스 거리를 계산한다.
- 마할라노비스 거리가 가장 작은 클러스터를 선택한다.
- 마할라노비스 거리가 임계값(예: 2 표준 편차)보다 작은 경우, \( p \)를 해당 클러스터에 추가한다. 
- 만약 마할라노비스 거리가 임계값 보다 클 경우 순서에 따라 CS,RS에 앞에서 설명 및 언급했던 할당하는 과정을 거친다.

### Q2
두 CS 집합(미니 클러스터)을 병합해야 하는가?

- 병합된 서브클러스터의 분산을 계산한다.
  - \( N \), \( \text{SUM} \), \( \text{SUMSQ} \)를 사용하여 빠르게 계산할 수 있다.
- 병합된 서브 클러스터의 분산이 임계값 이하인 경우 병합한다.
- 임계값 보다 클 경우 순서에 따라 CS,RS에 앞에서 설명 및 언급했던 할당하는 과정을 거친다.


# The CURE Algorithm
- Extension of k-means to clusters of **arbitrary shapes**
  
  - 센트로이드 기반
    - 점들간의 거리의 평균을 계산하여 구하므로 필연적으로 클러스터(군집)가 구 모양을 형성함
      - 문제점은 만약 실제 데이터의 군집이 구형태를 따르지 않는다면 예측성능이 저하됨
    ![image](https://github.com/user-attachments/assets/113a712d-639c-458c-a064-c44bedb776fc)

### BFR/k-means의 문제점
- 각 차원에서 클러스터가 정규 분포한다고 가정한다.
- 비구형 또는 임의의 형태의 클러스터에 대해 잘 작동하지 않는다.
- 이상치에 매우 민감하다.
- 클러스터링 결과가 각 클러스터의 표현(중심점 기반, 모든 점) 방식에 크게 의존한다.

![image](https://github.com/user-attachments/assets/35ce9b90-49b8-4878-9dff-5e1670ecbaee)

## CURE (Clustering Using REpresentatives)

- 유클리드 거리를 가정한다.
- 클러스터가 임의의 형태를 가질 수 있도록 허용한다.
- 클러스터를 표현하기 위해 중심점 대신 **대표 점들**의 집합을 사용한다.
- 센트로이드 기반 접근법과 모든 점을 고려하는 접근법을 혼합한 접근법이다.
    - alpha =0 then -> centroid elif alpha =1 then all-point aproach
![image](https://github.com/user-attachments/assets/7eeea1e0-1396-4bdb-8232-6f9e5bc0b445)

## Starting CURE: Two-pass Algorithm

### Pass 1: Initialization

1. 메인 메모리에 맞는 랜덤 샘플 점들을 선택한다.
   - `sample_points = random_sample(points)`

2. 초기 클러스터:
   - 샘플 점들을 `계층적`으로 클러스터링한다.
     - `initial_clusters = hierarchical_clustering(sample_points)`
   - 가장 가까운 점/클러스터를 그룹화한다.

3. 각 클러스터에 대해 `대표 점`들을 선택한다.
   - 가능한 한 분산된<멀리 떨어진> 샘플 점들을 선택한다.
     - `dispersed_points = pick_dispersed_points(cluster)`
   - 샘플에서 대표 점들을 클러스터 중심<방향>으로 α 비율만큼 이동시킨다.
     - `centroid = calculate_centroid(cluster)`
     - `new_point = move_toward_centroid(point, centroid, alpha)`
   - α = 0이면, CURE는 모든 점을 고려하는 표현과 유사하게 동작한다.
   - α = 1이면, CURE는 중심점 기반 접근법으로 축소된다.
   - 이 방법은 군집의 크기를 감소시키므로 중심에서 멀리 떨어진 이상치에 덜 민감하게 만든다.

![image](https://github.com/user-attachments/assets/0cebbc96-0d21-4751-a82f-9e1f435882bd)

![image](https://github.com/user-attachments/assets/9e81db73-f8a9-489d-b0a1-19aa6ae03bde)

### Pass 2: Merge

1. 전체 데이터셋을 다시 스캔하고 각 점 \( p \)를 확인한다.

2. 점 할당: \( p \)를 "가장 가까운 클러스터"에 배치한다.
   - "가장 가까운"의 일반적인 정의: \( p \)와 가장 가까운 `대표 점`<가능 한 가장 멀리 떨어져 있는>을 찾아 해당 `대표 점의 클러스터에 할당`한다.
   - ![image](https://github.com/user-attachments/assets/f3332233-6d45-43d1-a407-72597254e6f9)
   - 즉, 각 점 \( p \)을 보조 저장소에서 가져와 대표 점들과 비교하여 할당한다.
  
## 정리
### 클러스터링

주어진 점 집합과 점들 간의 거리를 바탕으로, 점들을 몇 개의 클러스터로 그룹화한다.

### 알고리즘

##### 병합적 계층 군집화 (Agglomerative Hierarchical Clustering)
- 센트로이드와 클러스트로이드

##### K-MEANS (k-means)
- 초기화, k값 선택

##### BFR (Bradley-Fayyad-Reina)
- 대규모 데이터셋 처리에 적합한 k-means 변형 알고리즘

##### CURE (Clustering Using REpresentatives)
- 임의의 형태의 클러스터를 처리할 수 있는 알고리즘
- 대표 점들을 사용하여 클러스터를 표현



