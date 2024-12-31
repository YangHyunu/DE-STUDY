# HDFS의 한계점 

## 맵-리듀스 방법의 한계
![alt text](이미지/image-77.png)

- 성능 문제: 
  - **I/O**, 노드간의 높은 통신 비용, 직렬화로 인해 오버헤드발생 등으로 시스템이 느려질 수 있다.

- `비효율적인 작업 유형`:

  - 반복 알고리즘: 머신 러닝, 그래프 및 네트워크 분석과 같은 `반복적인 계산 작업`.
    - **반복** -> 맵작업 -> I/O
  - 인터랙티브 데이터 마이닝: 검색<Elasticsearch>과 같은 **실시간** 인터랙티브 데이터 마이닝 작업.
  -  배치프로세싱을 지원하지 , 인터렉티브 프로세싱을 지원하지 않는다.

## 약점과 한계
1. **효율성 문제**
높은 통신 비용: 노드 간 데이터 전송이 많아 네트워크 통신 비용이 높다.
빈번한 디스크 쓰기: 출력 결과를 디스크에 자주 기록해야 하므로 성능이 저하된다.
메인 메모리 활용 제한: 메인 메모리를 충분히 활용하지 못한다.
    -> I/O를 줄일 수 없다.

1. **프로그래밍 모델 문제**
구현 어려움: 모든 작업을 MapReduce 프로그램으로 구현하기 어렵다.
복잡한 작업: 간단한 작업도 `여러 단계`의 MapReduce 작업이 필요할 수 있다.
    - 맵 혹은 리듀스가 필요하지 않은 작업도 반드시 맵-리듀서를 사용해야한다.
제어 구조 및 데이터 타입 부족: 제어 구조와 데이터 타입이 제한적이다.


3. **실시간 처리 문제**
    전체 입력 스캔 필요: MapReduce 작업은 전체 입력 데이터를 스캔해야 한다.
    - 현재에서 일컬어 지는 빅데이터는 단순히 큰 데이터가 아닌 엄청난 빈도로 들어오는 `실시간`데이터를 의미한다.
    스트림 처리 및 랜덤 접근 불가: 스트림 처리와 랜덤 접근이 불가능하다.
    - 맵-리듀스 작업중에 작업되는 데이터에 접근할 수 없고, 그저 완료될때까지 기다릴 수 밖에 없다.

##### 요약
- 효율성 문제: 높은 통신 비용, 빈번한 디스크 쓰기, 메인 메모리 활용 제한.
- 프로그래밍 모델 문제: 구현 어려움, 복잡한 작업, 제어 구조 및 데이터 타입 부족.
- 실시간 처리 문제: 전체 입력 스캔 필요, 스트림 처리 및 랜덤 접근 불가.

---

## Solution ?
    -> I/O와 오버헤드를 줄이기 위해 데이터를 `메모리`에서 I/O 처리하자.
    -> 하드 디스크를 SSD로 교체해서 I/O속도 및 CPU의 부하를 줄이자.

![alt text](이미지/image-78.png)

### 빅데이터 분석에서의 MapReduce의 역할과 한계

- **MapReduce의 기여**:  
  MapReduce는 빅데이터 분석을 크게 단순화시켰다.

- **MapReduce의 한계**:  
  MapReduce는 배치 처리(batch processing)에만 적합하다.

- **MapReduce가 인기를 얻으며 사용자가 요구한 추가 기능**:  
  - 더 복잡한 다단계 애플리케이션  
    - 예: 반복적인 그래프 알고리즘 및 머신러닝
  - 범용 클러스터 컴퓨팅 시스템
  - 실시간 데이터 및 배치 처리
  - 더욱 상호작용적인 애드혹(ad-hoc) 쿼리

- **다단계와 상호작용형 애플리케이션의 공통 요구사항**:  
  - 병렬 작업(parallel jobs) 간의 더 빠른 데이터 공유 필요


![alt text](이미지/image-82.png)


## Spark Architecture
![alt text](이미지/image-83.png)

![alt text](이미지/image-84.png)

- SparkContext가 태스크에 필요한 요구사항을 Cluster Manager에 전달하면 Cluster Manager가 각 노드에 명령을 전달하고 관리함. 

### Spark 구성 요소

#### SparkContext
- 드라이버 프로그램 내부의 하나의 클래스 객체
- **주요 진입점**: Spark 기능의 주요 진입점.
- **클러스터 연결**: Spark 클러스터에 대한 연결을 나타냄.
- **클러스터 접근**: Spark에게 클러스터에 어떻게 접근할지, 어디에 접근할지를 알려줌.
- **RDD 및 브로드캐스트 변수 생성**: 클러스터에서 RDD와 브로드캐스트 변수를 생성할 수 있음.
- RDD 란 데이터를 일정한 사이즈로 스플릿(파티셔닝)을 해 클러스터에 전달된 청크들의 집합을 의미함

#### Driver Program
- **주요 프로세스**: SparkContext 객체에 의해 조정되는 주요 프로세스.
- **설정 가능**: 특정 매개변수로 Spark 프로세스를 구성할 수 있음.
- **Spark 작업 실행**: Spark 작업은 Driver에서 실행됨.
-> 태스크를 쪼개고 스케쥴링을 하여 워커노드에 알려주는 역할은 클러스터 매니저를 통해 드라이버 프로그램 내부의 스파크 컨텍스트가 담당함
#### Application
- **애플리케이션**: Driver 프로그램 + Executors. -> 하둡에서의 맵과 리듀스


#### Cluster Manager
- **클러스터 관리자**: 클러스터의 `리소스를 관리`하는 외부 서비스 (Standalone Manager, YARN, Apache Mesos, Kubernetes).

#### Deploy Mode
- **배포 모드**: 드라이버가 배포 환경에서 실행되는 위치를 지정함.

##### Client Mode (기본값)
- **클라이언트 모드**: 드라이버 `데몬`이 Spark 작업을 클러스터에 전달하는 머신에서 실행됨.
  - **장점**: 사용자 입력을 받거나 쉘 명령을 사용할 때 유용함.
  - **리소스**: 클러스터에서 드라이버 데몬을 위한 리소스를 예약할 필요가 없음.

##### Cluster Mode
- **클러스터 모드**: 드라이버가 클러스터의 임의의 노드에서 실행됨.
  - **단점**: Spark 작업을 인터랙티브하게 사용할 수 없음.
  - **리소스**: 클러스터에서 드라이버 데몬 프로세스를 위한 리소스를 예약해야 함.


##### Mesos
- YARN과 매우 유사하나, 차이점은 Mesos는 OS단에서 실행되고, YARN은 이후 애플리케이션 계층에서 실행되는 차이점이 있음

###### 쿠버네티스
- 도커 및 컨테이너의 리소스 관리를 하는 역할을 함
An external service to manage resources on the cluster(standalone, YARN,Apache Mesos,Kubernetes)
- Standalone L good for small Spark clusters, not good for bigger cluster(i.e, enterprise context)

데몬 형태로 계속 실행되고 있으므로, 클러스터가 많은 경우 필요하지 않은 리소스를 항상 잡아먹는 문제가 있음 

- YARN and Mesos: no deamon overhead (better performance and sacalability), general purpose distributed resource menagemant
- YARN is specially designed for Hadoop workloads
 - Application level scheduler
 - Mesos is designed for all kinds of workloads
  -  OS level scheduler 

Kubernetes: open source system for automating deployment,scailing, and management of containerized applications.
- Used for running Spark applications in containerized fashion -> good option to deploy Spark applications in Cloud enviorment

클라우드 서비스 의 기본은 가상화 -> OS의 가상화 
따라서 OS를 가상화 시킨 컨테이너를 관리하느 쿠버네티스의 사용률이 점점 높아지고 있음



![alt text](이미지/image-85.png)
- 스파크 컨텍스트와 워커 노드의 익세큐터가 직접 통신하기도 함 -> 각 태스크의 완료 및 상태를 전달 
---
![alt text](이미지/image-130.png)
### Internals of job execution in Spark.
- Drive Program이 실행되면서 SparkContext 객체를 생성함
- Spark Context는 job이 주어지면 **DAG scheduler**를 통해 job을 RDD를 분석하여 효율적으로 테스크를 실행하기 위한 계획(어떻게 스플릿 할지 워커노드를 몇개 생성할지 ) 및 설계도를 만듬
- **Spark Context**가 만들어놓은 **DAG scheduler**를 Cluster Manager에 전달해 job을 파티셔닝하고, 워커노드를 생성하여 task를 전달함.

![alt text](이미지/image-86.png)

### Resilient Distributed Dataset (RDD)

- **분산 객체 컬렉션**: RDD는 클러스터의 여러 노드에 걸쳐 분산 저장되는 객체들의 집합이다.
- **데이터 연산**: 모든 데이터 연산은 RDD를 기반으로 수행된다.
- **불변성**: RDD는 한 번 생성되면 **절대로 변경할 수 없다**(Immutable).
- **메모리 및 디스크 저장**: RDD는 메모리나 디스크에 저장할 수 있다.
- **장애 복구(Fault Tolerance)**: RDD는 lineage 정보를 통해 장애가 발생했을 때 데이터를 복구할 수 있다.
- **lineage information** 각 RDD는 기존 RDD에 sort 및 operation을 통해 새롭게 생성되는 구조, 즉. 각 RDD는 자신의 부모 노드(RDD)와 부모 노드에 어떤 Operation을 통해 자신이 생성됬는지 정보를 가짐. -> 즉, 자식 노드(RDD)가 고장나더라도 고장난 노드는 자신의 부모 및 Operation정보를 알고 있으므로, 부모노드로 부터 동일한 Operation을 통해 재생할 수 있음 -> 장애복구 * 대신 부모노드는 당연히 변경불가능 해야함.
### RDD 생성 방법
- **Python 컬렉션 병렬화**: Python 컬렉션(리스트 등)을 병렬화하여 생성한다.
- **기존 RDD 변환**: 기존 RDD를 변환(transform)하여 생성한다.
- **파일에서 생성**: HDFS 또는 S3, HBase 등 Hadoop을 지원하는 스토리지 시스템에서 파일을 읽어와 생성한다.
- **한번 생성된 RDD는 절대로 수정할 수 없음**
### 파티션 설정
- **파티션 수 지정**: 프로그래머가 RDD의 파티션 개수를 지정한다.
- **파티션 수와 클러스터 코어**: 일반적으로 RDD의 파티션 수는 클러스터의 CPU 코어 수와 동일하게 설정한다.

![alt text](이미지/image-131.png)
---
![alt text](이미지/image-88.png)

![alt text](이미지/image-89.png)
-> 기존의 데이터를 통해 임의의 Operation을 통해 `새로운 데이터를 생성`하는 것은 Transformation이라 칭함.
    -> Lazy operation:transformation은 어떤 Action이 수행되는 경우에만 실행됨
    즉, 앞에서 작성한 Map,Filter 등의 Operation은 Action을 만나 Action이 실행된 경우에 순차적으로 실행됨 -> 절대로 스스로 실행돼지 않음.
-> Action이랑 Operation의 최종결과 값을 Return하는 것 
-> Persistence
 - RDD는 태스크를 실행된 후 기본적으로 사라지게 되어있음
  - RDD를 하드디스크에 저장할 수도 있다.
  - RDD는 데이터 이므로 작업이 수행되다 보면 데이터가 지속적으로 증가하게됨 따라서 프로그래머가 RDD를 메모리에 캐시할지 결정할 수 있음.
  
![alt text](이미지/image-90.png)

 Spark also supports the speculative execution like Hadoop MapReduce.
 Need to deal with slow or failed tasks.
 By default, this feature is turned off.
 You can turn it on via configuration: spark.speculation = True
 How to identify ‘slow’ task?
 We can configure via spark.speculation.multiplier
 This value specify the times (i.e., multiplication) of speculation median values
 e.g., assuming median value = 3 and multiplier = 2, if the task takes
longer time than 6, the Spark system re-launches the same task

- 스파크도 하둡의 Speculative Execution과 유사한 기능을 제공함. 즉, 특정 노드의 테스크가 길어지면 태스크를 종료시키고 인근 노드로 대체함
- **느림** 얼마나 느린지 어떻게 결정할까

![alt text](이미지/image-91.png)

![alt text](이미지/image-92.png)
워드카운트 -> 하둡에 피해 훨씬 간단하다.

![alt text](이미지/image-93.png)

- flatMap은 Map처럼 결과물을 각 리스트로 반환하는게  아니라 
- 결과물을 하나의 리스트에 합쳐서 반환함.



![alt text](이미지/image-94.png)

![alt text](이미지/image-95.png)

![alt text](이미지/image-96.png)

Lazy operation의 장점:
RDD가 만들어 진후 Operation을 만나기전 아무것도 변하지 않음
엄청나게 많은 트랜스폼이 발생하더라도 부모 RDD의 안정성을 확보할 수 있다.

![alt text](이미지/image-97.png)

## Spark SQL
- 스파크를 위해 Apache Hive 를 기반으로 만든 SQL
- HIVE의 경우 기본적으로 HDFS 환경에서 실행되는 것을 기반으로 하기 때문에 (맵-리듀스) 느리고 무겁다는 문제가 있었음. 따라서 스파크 환경에 필요한 쿼리 랭귀지를 만든게 Spark SQL이다.

# Spark Streaming
하둡의 경우 스트리밍 데이터 처리에 대해 불 필요한 I/O과정으로 발생하는 오버헤드 문제가 있었으나
스파크의 경우 인메모리 프로세싱을 통해 I/O를 줄이고, 메모리에 배치사이즈로 데이터를 올려 처리하면서 오버헤드를 줄여 스트림 데이터에 적합함.

![alt text](이미지/image-98.png)

![alt text](이미지/image-99.png)