1. 주키퍼 실행 -> 주키퍼는 하둡 스파크의 Yarn 처럼 카프카 클러스터를 관리하는 역할을 한다.
```
./bin/zookeeper-server-start.sh config/zookeeper.properties
```
2. 카프카 실행
```
./bin/kafka-server-start.sh config/server.properties &
```
jps 명령어로 실행 확인
```
how30909@DESKTOP-QF7FIQJ:~/kafka_2.13-3.3.2$ jps
11939 QuorumPeerMain
12807 Jps
12363 Kafka
```
3. 토픽 생성  
bin/kafka-topics.sh --create --topic bit_topic --bootstrap-server localhost:9092
Created topic bit_topic.

4. 모니터링 ui 설치
docker 이미지 pull
docker pull provectuslabs/kafka-ui

```
version: '2'
services:
  kafka-ui:
    image: provectuslabs/kafka-ui
    container_name: kafka-ui
    ports:
      - "8090:8080"
    environment:
      - KAFKA_CLUSTERS_0_NAME=localhost-kafka
      - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=<실제 Kafka 브로커 IP>:9092  # 실제 Kafka 브로커 IP와 포트
      - KAFKA_CLUSTERS_0_ZOOKEEPER=localhost:2181               
```

#### 프로듀서 실행
```
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bit_topic
```
카프카 프로듀서 스크립트 실행 
```
(venv) PS C:\Users\LHW\DE> python kafka_producer.py
```
다음과 같은 형태의 출력이 나오면 정상적으로 프로듀서가 실행된 것이다.
``` json
Sent to Kafka: {'ticker': 'BTC-USD', 'price': np.float64(93693.9375), 'volume': 38489337856, 'timestamp': '2024-12-30T12:54:21Z'}
```
---

```
%3|1735563261.392|FAIL|stock-price-producer#producer-1| [thrd:localhost:9092/bootstrap]: localhost:9092/bootstrap: Connect to ipv4#127.0.0.1:9092 failed: Unknown error (after 2063ms in state CONNECT)
Sent to Kafka: {'ticker': 'BTC-USD', 'price': np.float64(93693.9375), 'volume': 38489337856, 'timestamp': '2024-12-30T12:54:21Z'}
Sent to Kafka: {'ticker': 'ETH-USD', 'price': np.float64(3400.709716796875), 'volume': 18586847232, 'timestamp': '2024-12-30T12:54:22Z'}
Sent to Kafka: {'ticker': 'DOGE-USD', 'price': np.float64(0.3209792375564575), 'volume': 2004904448, 'timestamp': '2024-12-30T12:54:23Z'}
```
---
#### 컨슈머 출력 확인
```
how30909@DESKTOP-QF7FIQJ:~/kafka_2.13-3.3.2$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bit_topic --from-beginning
```
---
```
{"ticker": "BTC-USD", "price": 93693.9375, "volume": 38489337856, "timestamp": "2024-12-30T12:54:21Z"}
{"ticker": "ETH-USD", "price": 3400.709716796875, "volume": 18586847232, "timestamp": "2024-12-30T12:54:22Z"}
{"ticker": "DOGE-USD", "price": 0.3209792375564575, "volume": 2004904448, "timestamp": "2024-12-30T12:54:23Z"}
{"ticker": "BTC-USD", "price": 93601.7265625, "volume": 38529232896, "timestamp": "2024-12-30T12:54:53Z"}
{"ticker": "ETH-USD", "price": 3400.142333984375, "volume": 18589278208, "timestamp": "2024-12-30T12:54:53Z"}
{"ticker": "DOGE-USD", "price": 0.3209792375564575, "volume": 2004904448, "timestamp": "2024-12-30T12:54:54Z"}
```
### 스크립트 형태로 컨슈머에 코인 가격이 정상적으로 입력되고, 컨슈머에서 출력되는 것을 확인하였다.

다음은 카프카 컨슈머를 Spark 혹은 데이터 웨어하우스에 연결하여 데이터를 저장하고 분석하는 과정을 진행할 것이다.