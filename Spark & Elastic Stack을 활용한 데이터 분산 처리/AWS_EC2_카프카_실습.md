# AWS EC2 실습
### 주의!! 가상 머신 사양을 프리티어가 아니라 조금 더 좋은 사양으로 하기 ! 이유는 낮은 사양에서는 잘 안됨.
Azure 가상 머신이랑 EC2 설정이랑 큰 차이가 없다. 
개인적으로 AWS는 처음이라 긴장했는데 클라우드 플랫폼이 기본 구조가 유사해서 괜찮았다
* 키 페어* 가 ssh 키인 것 같다. .pem파일 형식으로 했음
* .pem 파일을 따로 잘 저장해둬야 한다.
로컬 머신의 .pem파일을 리눅스에 넣기
```
scp -i /path/to/your_key.pem /path/to/file.pem 사용자이름@가상머신_PIP:~
```
###### 복사 화긴
```
how30909@DESKTOP-QF7FIQJ:~$ ls
 Airflow   Kafka.pem  'UBUNTU 환경에 접속해서 자바 11버전 설치하기.md'   kafka_2.13-3.3.2   kafka_2.13-3.3.2.tgz
```
![image](https://github.com/user-attachments/assets/3461c9a7-df6d-4b52-a3de-e59d805cf30f)
예: 붙여넣기 하면 서버에 접속됨

### 서버에 접속하기
##### jdk설치

```
sudo apt-get update
sudo apt-get install openjdk-11-jdk
```



##### ubuntu 사용시 bash 쉘 사용

### kafka 설치
1. mkdir 로 kafka 폴더 만들고 이동
`wget https://archive.apache.org/dist/kafka/3.3.2/kafka_2.13-3.3.2.tgz`

`tar -xvzf kafka_2.13-3.3.2.tgz`



#### kafka home
```
ubuntu@ip-172-31-14-133:~/kafka/kafka_2.13-3.3.2$ pwd
/home/ubuntu/kafka/kafka_2.13-3.3.2 복사
vi ~/.bashrc
```
입력한 후 맨 밑에
```yaml
vi .bashrc
......
export KAFKA_HOME=/home/ubuntu/kafka/kafka_2.13-3.3.2
......

exit
sudo su - kafka
```
입력후 
```
ubuntu@ip-172-31-14-133:~/kafka/kafka_2.13-3.3.2$ source ~/.bashrc
ubuntu@ip-172-31-14-133:~/kafka/kafka_2.13-3.3.2$ echo $KAFKA_HOME
로 경로설정이 제대로 됐는지 확인
```

### /etc/hosts 설정
```
sudo vi /etc/hosts
```
- root 디렉토리가 아니므로 sudo 를 넣어줘야 파일 수정한게 저장이 됨
```yaml
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts

{server_ip} kafka_node1
{server_ip} kafka_node2
{server_ip} kafka_node3
```
- 여기서 {server_ip}에 EC2 가상머신의 private-ip 넣기
자기자신의 host는 0.0.0.0

#### configuration

```
vi $KAFKA_HOME/config/server.properties
......
broker.id=1
......
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://kafka_node1:9092
......
log.dirs=/home/ubuntu/kafka/kafka_2.13-3.3.2/logs
......
zookeeper.connect=kafka_node1:2181,kafka_node2:2181,kafka_node3:2181
```

- mkdir data 하기


### Zookeeper추가 설정

```yaml
echo "1" > $KAFKA_HOME/data/myid
......
vi $KAFKA_HOME/config/zookeeper.properties
......
dataDir=/home/ubuntu/kafka/kafka_2.13-3.3.2/data
......
initLimit=20
syncLimit=5
server.1=kafka_node1:2888:3888
server.2=kafka_node2:2888:3888
server.3=kafka_node3:2888:3888
......
```

- myid `0` 으로 설정하게 되면 에러 발생
  - 1부터 시작하는 것을 권장 -> 이후 노드의 브로커아이디와 동일하게 맞출것

**initLimit**

- **follower** 가 leader와 처음 연결을 시도할 때 가지는 tick 횟수. **제한 횟수 넘으면 timeout**

**syncLimit**

- **follower** 가 leader와 연결 된 후에 앙상블 안에서 leader와의 연결을 유지하기 위한 tick 횟수
- **제한 횟수 넘으면 time out**

**server.(zookeeper_server.pid의 내용)=(host name 이나 host ip):2888:3888**

- **앙상블**을 이루기 위한 서버의 정보
- 2888은 동기화를 위한 포트, 3888은 클러스터 구성시 leader를 산출하기 위한 포트
- 여기서 서버의 id 를 dataDir 에 설정해 줘야 한다.

## ZooKeeper 설정 역할 테이블

| 설정 이름      | 역할                           | 설명                                                                                                         |
|---------------|--------------------------------|--------------------------------------------------------------------------------------------------------------|
| **initLimit** | 최초 연결 시 최대 허용 시간     | 팔로워가 리더와 **처음 연결**할 때 사용할 수 있는 최대 tick 횟수를 설정하는 옵션. 제한 시간을 초과하면 연결 시도가 타임아웃됨. |
| **syncLimit** | 연결 유지 시 최대 허용 시간     | 팔로워가 리더와 **연결된 후** 주기적으로 상태 동기화를 위해 사용할 최대 tick 횟수를 설정. 제한 시간을 초과하면 연결이 타임아웃됨. |
| **server.x 설정** | ZooKeeper 앙상블 구성        | 앙상블 내 각 서버의 ID와 호스트 정보를 설정하는 옵션. **동기화 포트(2888)**와 **리더 선출 포트(3888)**를 포함하여, 서버 간 통신 및 리더 선출을 위한 경로를 정의함. |

---

## ZooKeeper와 Hadoop의 리더-팔로워 및 네임노드-데이터노드 구조 비교

| 시스템         | 주요 구성 요소                  | 역할                                                                                                 |
|---------------|--------------------------------|------------------------------------------------------------------------------------------------------|
| **ZooKeeper** | 리더, 팔로워                    | 리더가 클러스터에서 **쓰기를 담당**하고, 팔로워가 리더의 지시를 따라 **데이터를 복제**하며 **읽기 요청**을 처리 |
| **Hadoop**    | 네임노드(NameNode), 데이터노드(DataNode) | 네임노드는 **메타데이터**를 관리하고, 데이터노드는 **실제 데이터 블록을 저장**                                  |



### **보안그룹 생성 및 적용**
EC2에서 새로운 보안그룹 생성 하기

![image](https://github.com/user-attachments/assets/297dac6b-6503-4b49-969a-b3cf72845673)
- 실습이기 때문에 0.0.0.0 , ::/0 모든 포트를 열었음. 실습이후 닫을 예정
###### ** 인바운드 규칙에도 동일하게!**
![image](https://github.com/user-attachments/assets/632cc7d1-30dc-471b-bf8a-a8cee95f22ad)
- 기존 인스턴스에 보안그룹 추가
  - EC2 >인스턴스> 인스턴스 ID> 보안 그룹 변경

### **인스턴스 이미지 생성**
- EC2 >인스턴스 > 인스턴스 ID > 이미지 생성
- 이미 생성 후 AMI들어가서 진행상황 화긴
![image](https://github.com/user-attachments/assets/bde33b15-5df4-4dd9-a5ff-f8a1a06c27ab)
- 이미지가 복사되는데 5-10분 정도 시간이 소요
![image](https://github.com/user-attachments/assets/e7c329e1-1013-4564-bbf8-2aeee97ac8f1)
- 인스턴스 시작> 새로운 인스턴스를 내  AMI 클릭 후 미리 만들어 둔 이미지를 선택해서 생성하기 , 기존 보안 그룹 선택, 키 페어는 기존에 있던것으로 사용
  - 인스턴스의 수는 2로 설정
![image](https://github.com/user-attachments/assets/1cfa6662-eab4-4cc9-8553-85f868ed6acb)

1. 터미널 2개를 추가로 열어서 앞에서 한 것처럼 각각 인스턴스 서버에 접속 
2. 각자 터미널에서 sudo vi /etc/hosts 를 입력 한 후 아까 채우지 않았던 각 인스턴스의 ip주소를 노드에 입력하기
3. kafka/kafka_2.13-3.3.2 에서 vi config/server.properties로 원래 노드가 broker_id  가 1이므로 나머지는 2 3으로 변경 & advertised.listeners node의 수를 broker_id에 맞게 변경후  wq
4. 각자 data -> vi myid 로 각자 자신의 broker_id를 맨 위에 입력후 wq
### **인스턴스 설정수정**

```yaml
# kafka_node2
echo "2" > $KAFKA_HOME/data/myid
......
vi $KAFKA_HOME/config/server.properties
......
broker.id=2
......

# ssh kafka_node2
echo "3" > $KAFKA_HOME/data/myid

vi $KAFKA_HOME/config/server.properties
......
broker.id=3
......
```
이제 각 우분투 서버에서 카프카와 주키퍼 실행 
### 인스턴스 실행

```yaml
# kafka_node1
$KAFKA_HOME/bin/zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties
$KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties

# kafka_node2
$KAFKA_HOME/bin/zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties
$KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties

# kafka_node3
$KAFKA_HOME/bin/zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties
$KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties
```

### 각자 토픽생성 <kafka_node입력 주의>
```
bin/kafka-topics.sh --create --bootstrap-server <kafka_node입력 주의>:9092 --replication-factor 1 --partitions 5 --topic hello
```

### 토픽 확인
```
./bin/kafka-topics.sh --list --bootstrap-server <kafka_node입력 주의>:9092
```
### 토픽 삭제
```
./bin/kafka-topics.sh --delete -topic data --bootstrap-server <kafka_node입력 주의>:9092
```
### 프로듀서
```
./bin/kafka-console-producer.sh --bootstrap-server <kafka_node입력 주의>:9092 --topic hello
```
나는 프로듀서는 kafka_node1에
### 컨슈머
```
./bin/kafka-console-consumer.sh --bootstrap-server <kafka_node입력 주의>:9092 --topic hello
```
컨슈머는 kafka_node2에 만들어 줬음


### 실행 결과 
![image](https://github.com/user-attachments/assets/55b85ab0-e9df-4156-b3c0-87ca6601a7f6)

- 노드 1에서 생성된 프로듀서: 노드 1에서 실행된 Kafka 프로듀서가 hello라는 주제로 메시지를 생성하고 있다. 이 프로듀서는 "Hello, node3!!!! From node1"이라는 메시지를 전송했음

- 노드 3에서 생성된 컨슈머: 노드 3에서 실행된 Kafka 컨슈머가 동일한 주제인 hello를 구독하고 있으며, 노드 1에서 보낸 메시지를 성공적으로 수신했다.

## 의의
- **이 과정**은 분산 시스템에서의 메시지 전송 및 처리의 예로, `Kafka의 주제를 통해 여러 노드 간의 통신을 효율적으로 관리할 수 있음을 보여준다`. 노드 1에서 생성된 메시지가 노드 3에서 성공적으로 소비되는 것이 확인됨
- 즉, **프로듀서**가 `다른 노드`에 있는 **컨슈머**와 어떻게 데이터를 교환하는지를 잘 나타내며, Kafka의 강력한 분산 처리 능력을 보여줌
  
