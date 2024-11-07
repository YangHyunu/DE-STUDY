# 카프카 모니터링 툴 설치

### UI for Kafka를 사용

[https://github.com/provectus/kafka-ui](https://github.com/provectus/kafka-ui)

### docker 이미지 pull

`docker pull provectuslabs/kafka-ui`

### docker image 확인

`docker image ls`

### docker compose

> Docker Compose는 **여러 컨테이너를 가지는 애플리케이션을 통합적으로 Docker 이미지를 만들고, 만들어진 각각의 컨테이너를 시작 및 중지하는 등의 작업을 더 쉽게 수행할 수 있도록 도와주는 도구**
> 

**docker-compose.yml** 이 필요함

`mkdir ui-for-kafka`

`vim docker-compose.yml`

github yml 참조

```yaml
version: '2'
services:
  kafka-ui:
    image: provectuslabs/kafka-ui
    container_name: kafka-ui
    ports:
      - "8090:8080"
    environment:
      - KAFKA_CLUSTERS_0_NAME=localhost-kafka
      - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=<자신의 아이피>:9092  # 실제 Kafka 브로커 IP와 포트
      - KAFKA_CLUSTERS_0_ZOOKEEPER=localhost:2181                                                               
```

이대로 실행하면? 제대로 붙지가 않음, 에러가 발생

물론 zookpeeper와 kafka는 실행이 되어있어야 함
#### 주키퍼 실행
뒤에 &옵션으로 -d 즉 데몬상태로 돌아가게 만듬
`$ cd kafka_2.13-3.3.2`
`$ ./bin/zookeeper-server-start.sh config/zookeeper.properties &`

#### kafka 실행

`$ cd kafka_2.13-3.3.2`
`$ bin/kafka-server-start.sh config/server.properties &`

### config 설정

`vim config/server.properties`

```yaml
#listeners=PLAINTEXT://:9092
#advertised.listeners=PLAINTEXT://your.host.name:9092

listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://<자신의 아이피>:9092
```

- listeners의 역할 : 내부에 연결할 IP, 카프카 브로커가 내부적으로 바인딩하는 주소
- advertised.listeners의 역할: 카프카 클라이언트나 커맨드 라인 툴을 브로커와 연결할 때 사용
  

<details>
<summary> 토글: 아래는 Windows 나 Mac 환경에서 필요한 설정, 나는 우분투를 사용해서 필요 X</summary>
<div markdown="1">
### docker-compose.yml 설정대로 하면 연결이 안되는 이유

### docker - [localhost](http://localhost) 연결

![alt text](image-5.png)

- [localhost](http://localhost) 9092로 연결하려고 시도!
    - 하지만 docker container내에 있는 localhost에 연결을 하게됨
    - 진짜 localhost가 어디인지 알려주자!
![alt text](image-1.png)
localhost:8090 에 접속은 되지만 제대로 토픽에 연결이 안되고 있음을 확인할 수 있다.
### extra_hosts와 host.docker.internal

- host.docker.internal를 사용해야 진짜 localhost에 접근이 가능함
- host.docker.internal 를 위해서는 host-gateway가 필요
- host-gateway를 사용해서 도커 컨테이너와 로컬을 연결하는 것

extra_host를 통해 host-gateway를 열어주고 host.docker.internal를 사용해준다
</div>
</details>


```
ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
```
```
vim config/server.properties 입력하고 
listeners=PLAINTEXT://:9092 부분 주석처리 풀고 아까 바꾼 localhost:9092를
위에서 확인한 자신의 ip:9092로 바꾼후에 
다시  현재 실행중인 kafka 종료 후 재실행 
ps -ef |grep kafka 입력 후 -> 도커 컴포즈 업..
```
![image](https://github.com/user-attachments/assets/15723428-df1d-422e-bb8e-b41a98242516)
