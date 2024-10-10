# What is Hadoop?

1. 오픈 소스 데이터 저장 및 처리 프레임워크
2. 대규모 확장 가능하고 자동으로 병렬 처리할 수 있음
- Based on work from Google
- GFS + MapReduce + BigTable
- Current Distributions based on Open Source and Vendor Work
    
    

### **RDBMS vs. Hadoop**

| **Category** | **Traditional RDBMS** | **Hadoop / MapReduce** |
| --- | --- | --- |
| **Data Size** | Gigabytes (Terabytes) | Petabytes (Hexabytes) |
| **Access** | Interactive and Batch | Batch – NOT Interactive |
| **Updates** | Read / Write many times | Write once, Read many times |
| **Structure** | Static Schema | Dynamic Schema |
| **Integrity<무결성>** | High (ACID) | Low |
| **Scaling<확장성>** | Nonlinear | Linear |
| **Query Response Time** | Can be near immediate | Has latency (due to batch processing) |
- **ACID**: Atomicity, Consistency, Isolation, Durability

## Why Use Hadoop?

- 싸다
    - 매우 저렴한 비용으로 대규모로 확장가능하다
- 빠르다
    - 데이터 처리를 병렬처리하므로
- 특정한 타입의 빅데이터 처리에 특히 최적화 되어있다.

# Hadoop: Apache 프레임워크 세트의 일부, 그 이상

Hadoop은 단순히 분산 처리를 지원하는 시스템이 아니라 다양한 기능을 지원하는 Apache 프레임워크의 집합.

![스크린샷 2024-09-24 151727](https://github.com/user-attachments/assets/0b2c5018-3320-483d-a370-f4172c0444e5)

### 1. 데이터 스토리지 (HDFS)

### 2. 데이터 처리 (MapReduce)

### 3. 기타 도구 및 프레임워크

- **데이터 접근(Data Access)**
    - **HBase**, **Hive**, **Pig**, **Mahout** 등 다양한 도구가 Hadoop과 통합되어 데이터를 쉽게 처리하고 쿼리할 수 있게 도와줌.
- **도구 (Tools)**
    - **Hue**, **Sqoop**, **Flume**은 데이터 수집, 변환, 모니터링 등을 위한 도구들.
- **모니터링 (Monitoring)**
    - **Greenplum**, **Cloudera**와 같은 도구를 사용하여 Hadoop 클러스터의 상태를 모니터링하고 알림을 받을 수 있다.

### 4. 전체 스택 구조

Hadoop은 다음과 같은 계층적 구조로 이루어져 있습니다:

- **Monitoring & Alerting**: 클러스터 상태 모니터링과 경고 시스템.
- **Tools & Libraries**: 다양한 데이터 처리 및 관리 도구.
- **Data Access**: Hive, HBase 등과 같은 데이터 접근 프레임워크.
- **MapReduce API**: 병렬 데이터를 처리하기 위한 분산 처리 프레임워크.
- **Hadoop Core - HDFS**: 대용량 데이터 스토리지를 지원하는 핵심 파일 시스템.

## **Core parts of Hadoop distribution**

![스크린샷 2024-09-24 153528](https://github.com/user-attachments/assets/d9dc7266-6401-4228-bf96-739cafa6eb9f)

# 하둡 에코 시스템

단순히 분산파일 시스템인 하둡만 쓰는게 아니라 , 현재 테스크에서 요구하는 기능을 지원하는 하둡 에코 시스템 내의 도를 이용하여 데이터를 처리하게 됨 

## 주요 구성 요소:

### 1. **저장(Storage)**

- **HDFS (Hadoop Distributed File System)**: 대규모 데이터를 분산 저장하는 파일 시스템임.

### 2. **리소스 관리(Resource Management)**

- **YARN**: 클러스터 리소스를 관리하며, 여러 애플리케이션이 동시에 실행될 수 있도록 지원함.

### 3. **데이터 처리 및 분석 도구**

- **MapReduce**: 병렬 분산 처리 프레임워크로, 대용량 데이터를 처리하는 데 사용됨.
- **Hive & Drill**: Hadoop에서 SQL을 사용하여 데이터를 쿼리할 수 있게 해주는 도구임.
- **Pig**: 데이터 흐름을 정의하기 위한 스크립팅 언어를 제공하는 도구임.
- **Mahout & Spark MLlib**: 기계 학습용 라이브러리로, 대규모 데이터를 학습하고 분석하는 데 사용됨.
- **Spark**: 인메모리 기반 데이터 처리 엔진으로, 매우 빠른 속도로 데이터를 처리할 수 있음.
- **Kafka & Storm**: 실시간 스트리밍 데이터를 처리하는 데 사용되는 도구들임.
- **HBase**: NoSQL 분산 데이터베이스로, 대규모의 구조화되지 않은 데이터를 처리하는 데 적합함.
- **Solr & Lucene**: 데이터 검색 및 색인을 위한 도구임.
- **Oozie**: 워크플로우 관리 도구로, 데이터 처리 작업을 스케줄링하는 데 사용됨.
- **Zookeeper & Ambari**: 클러스터 관리 및 설정 조정을 위한 도구임.

### 4. **데이터 전송 도구**

- **Flume**: 비정형 또는 반정형 데이터를 HDFS와 같은 저장 시스템으로 수집하고 전송함.

### Apache SPARK

기존 하둡의 맵-리듀스로는 반복적인  데이터 처리를 요구하는 머신러닝 프로세스에 적합하지 않음 

스파크는 인메모리 프로세싱을 지원하여 전체 데이터를 메모리에 적재하여 사용함

빠르고 범용적인 인메모리 기반 데이터 처리 엔진. 데이터를 메모리에 저장한 상태에서 연산을 수행하기 때문에, 기존의 디스크 기반 처리 방식에 비해 매우 빠르게 데이터를 처리할 수 있음.

### Apache Kafka

LinkedIn에서 개발, 대량의 실시간 이벤트 데이터를 처리해야 할 때, 기존 메시지 큐 시스템들은 확장성과 내구성이 부족했음. 이를 해결하기 위해 대규모 데이터를 실시간으로 전송하고 처리할 수 있는 시스템이 필요했음.

- **메시지 큐** : 분산화된 환경에서 발신자와 수신자 사이에 메시지를 전송하고, 수신하는 기술
- **실시간 데이터 스트리밍**: 실시간으로 데이터를 전송하고 처리하는 데 최적화되어 있으며, 로그 데이터나 이벤트 데이터를 실시간으로 처리하는 환경에서 많이 사용.
- **확장성**: 수평적으로 확장 가능해 대규모 데이터 스트림을 처리하는 데 적합.
- **내구성**: 데이터를 안전하게 저장하고 복구할 수 있는 구조를 갖추고 있어 안정적인 데이터 처리가 가능.

### **Apache Hive**

Hive는 *SQL과 유사한 쿼리 기능을 제공하는 분산 데이터 웨어하우스 시스템으로,*

RDB의 데이터베이스, 테이블과 같은 형태로 HDFS에 저장된 데이터의 구조를 정의하는 방법을 제공하며, 이 데이터를 대상으로 SQL과 유사한 HiveQL 쿼리를 이용하여 데이터를 조회하는 방법을 제공

- **SQL 기반 쿼리**: HiveQL을 사용해 SQL처럼 데이터를 쉽게 쿼리 가능.
- **대규모 데이터 처리**: 주로 데이터 웨어하우스 애플리케이션에서 사용.
- **Hadoop과의 통합**: Hadoop의 MapReduce를 이용해 쿼리를 실행.

### **Apache HBase**

대용량의 실시간 데이터를 처리할 필요성이 커지면서, 비정형 데이터 처리와 빠른 읽기/쓰기 작업을 지원하는 NoSQL 데이터베이스가 요구되어 구글의 BigTable을 기반으로 설계

Base는 스키마 없는 데이터베이스에서 대량의 데이터에 대해 임의 액세스 및 강력한 일관성을 제공하며, 데이터는 개별 열에 저장되고 고유한 행의 key로 인덱싱됨

- **실시간 읽기/쓰기**: 빠른 응답 속도를 요구하는 애플리케이션에 적합.
- **수평 확장성**: 노드를 추가해 데이터베이스를 확장 가능.
- **비정형 데이터 처리**: 고정된 스키마가 없어 유연한 데이터 관리가 가능.
- **랜덤 액세스**: 특정 데이터를 빠르게 조회할 수 있음.

![스크린샷 2024-09-24 155417](https://github.com/user-attachments/assets/e3da94ba-d5bb-4fae-867f-6535414ad9cb)
### Master: **JobTracker**

- **역할**: 클러스터에서 MapReduce 작업을 관리하는 마스터 노드 역할을 수행.
    - **MapReduce 작업 제어**: 클러스터에서 실행되는 모든 MapReduce 작업을 관리하는 역할을 함.
    - **작업 할당**: 클러스터의 다른 노드에 있는 **TaskTracker**에 Map 및 Reduce 작업을 할당.
    - **작업 모니터링**: 작업이 실행되는 동안 이를 모니터링하고, 진행 상황을 추적.
    - **실패한 작업 재시작**: 클러스터 내에서 실패한 작업을 다른 노드에서 다시 실행하도록 함.
    - 
![스크린샷 2024-09-24 155900](https://github.com/user-attachments/assets/ea06ca72-0095-4041-a21c-5c3872237689)

### Slave: **TaskTracker**

- **역할**: 각 슬레이브 노드에서 개별적으로 MapReduce 작업을 실행하고 JobTracker와 통신.
    - **단일 TaskTracker**: 슬레이브 노드당 하나의 TaskTracker가 할당 됨.
    - **작업 실행 관리**: 각 노드에서 개별 작업을 실행하고 관리.
    - **병렬 처리 지원**: 여러 JVM을 인스턴스화하여 병렬로 작업을 처리할 수 있음.
    - **JobTracker와의 통신**: **Heartbeat**를 통해 JobTracker와 통신하여 상태를 보고하며 태스크를 판단함.
