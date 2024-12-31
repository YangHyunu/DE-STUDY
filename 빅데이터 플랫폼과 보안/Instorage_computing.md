# Instoraged_Computing

### 문제의식?
![alt text](image-5.png)]
#### DB던 BI던 데이터를 처리함에 있어 대부분의 병목현상이 입출력 `I/O` 에서 발생하더라

- 심지어 배치방식의 맵-리듀스 방식을 사용함에 있어서도 입-출력이 빈번하므로 병목현상이 많이 발생한다.

![alt text](image-6.png)

- 데이터를 이동하는 것보다 컴퓨팅을 데이터 근처로 이동시키는게 훨씬 효율적이다.

- 데이터의 이동을 줄임으로서 에너지와 성능을 높일 수 있다.

- 즉, 한마디로 데이터를 컴퓨팅하는 것 보다 데이터를 이동시키는데 더 많은 자원과 시간이 소모된다.

![alt text](image-7.png)

기존의 개선 방법들: 쿼리나 요청을 클라이언트가 했을 때 그 데이터의 처리와 계산을 호스트의 컴퓨터에서 하는것이 아니라 호스트의 컴퓨터에 전달돼기 전 일정한 태스크를 처리한 후 전달하는 방식으로 병목현상과 호스트컴퓨터의 cpu 작업량을 줄였다.

ex: 
- intelligent SSD 의 경우 SSD에 아주 작은 os를 넣어 SSD 내부의 데이터를 컨테이너 환경에서 애플리케이션을 실행함.

- Seagate: Seagate는 더욱 발전한 방식으로 SSD 내부의 NAND 메모리 에서 데이터를 처리하는 방식 
=> 계속해서 컴퓨팅 방식이 점점 데이터에 가까워 지는것을 알 수 있음

# What is ISC (In-Storage Computing)?
![alt text](image-8.png)
- 데이터 처리를 SSD 내부에서 하여 중간결과값이나 최종결과값만 호스트 컴퓨터에 전달해주자!

#### ISC의 장점
- I/O Traffic: 데이터 인근에서 처리하기 때문에 데이터 이동이 줄어듬
- Scalability: 데이터 처리를 SSD 내부에서 하기 때문에 호스트 컴퓨터의 cpu 작업량이 줄어듬 따라서 호스트의 cpu를 다른 작업에 더 많이 사용할 수 있음
- Architecture: 성능이 고성능일 필요가 없으므로 arm 아킽텍처를 사용하여 더욱 전기를 적게 사용할 수 있음 
- Bandwidth: 낮은 대역폭을 가진 SATA나 PCI Express 같은 I/O 인터페이스를 통해 데이터를 전송하는 방식보다 호스트에 데이터를 전달하는 속도가 훨씬 빠름

## Problem Statement

### Project goal
- 하둡 맵리듀스 프레임워크에 맞는 ISC를 설계하고 구현하는 것

### Suggested solution
- Mapper를 SSD에 올려서 SSD 내부에서 데이터를 처리하고, Reducer는 호스트의 컴퓨터에서 실행한다
- Reducer는 Mapper가 처리한 데이터를 받기 때문에 dependency가 발생하므로 여기에서 대부분의 병목현상이 발생하게 된다.
- 즉, Mapper가 최대한 빨리 데이터를 처리하고 Reducer가 그 데이터를 받아서 처리하는 방식으로 병목현상을 줄일 수 있다.

### Challenging problems
- Discrepancy in data representation

- Discrepancy in system interfaces

- Data split

- Feature offloading

- A pesudo fully distributed mode

### Contributions
- Real SSD implementation
- Hadoop system integration
- Exploration of the challenging issues

# SYSTEM DESIGN & DEMO
![alt text](image-9.png)
- SSDlet : SSD 내부에서 동작하는 프로그램
- ISC Runtime System: SSD 내부에서 구현된 프로그램 라이브러리
- Base Device Driver: SSD의 하드웨어를 제어하는 드라이버
- `API`: Host와 SSD간의 통신을 위한 API
- 'OPEN' , 'CLOSE' , 'GET, 'SET' ,'PUT' 등의 명령어를 사용하여 현재 프로세스를 제어할 수 있음

![alt text](image-10.png)


![alt text](image-11.png)

기존 방식에서는 호스트 컴퓨터에서 Mapper와 Reducer가 동시에 실행되었지만, ISC에서는 Mapper가 SSD 내부에서 실행되고 Reducer는 호스트 컴퓨터에서 실행된다. 
이러한 방식을 구현하기 위해 Interface layer를 만들어서 Mapper와 Reducer를 통신하게끔 만들었다.

## Workflow
![alt text](image-12.png)
1. 호스트에서 A.text라는 파일을 대상으로 Mapper를 실행하도록 명령함
2. SSD는 파일 시스템이 없기 때문에 A.text가 뭔지 알 수 없음 
3.이때, interface layer가 호스트로부터 A.text의 메타데이터를 받아서 SSD 내부의 A.text의 주소를 LBA로 변환하여 SSD에 전달함
4. Mapper는 A.text를 읽어서 처리한 후 작업완료를 interface layer에 알림
5. interface layer는 mapper가 처리한 중간결과값을 로컬파일시스템에 저장함
6. Mapper가 작업완료함을 호스트에 알림
7.Reducer가 Mapper가 처리한 중간결과값을 읽어서 처리함

## Design Challenges

### Discrapancy in data representation
- 호스트와 SSD간의 데이터 표현 방식이 다름
    - 호스트는 파일 시스템을 사용하여 데이터를 저장하지만 SSD는 파일 시스템이 없음
    - 따라서 호스트로부터 받은 데이터를 SSD 내부에서 어떻게 이해하여 처리할 것인지 문제가 발생함
- 해결방안
    - 이를 해결하기 위해 Interface layer를 만들어서 호스트로부터 받은 SSD 내부의 데이터 위치를 SSD 내부에서 이해할 수 있도록 LBA로 변환하여 SSD에 전달함

### Discrepancy in system interfaces
- 호스트의 하둡시스템은 자바를 사용하고, ISC는 C나 C++을 사용함
    -즉, 호스트와 SSD가 사용하는 언어가 달라 직접 통신할 수 없음
- 해결방안
    1. ISC 디바이스 내부에 작은 OS <JVM>을 넣어서 호스트와 통신하도록 함
    2. Software interface layer에서 JNI를 사용하여 호스트와 통신하도록 함
    - JNI는 자바와 C++간의 통신을 위한 인터페이스를 제공함

### Data split
- 하둡데이터 파일시스템은 한 청크를 64MB로 나누어서 저장함
    - 이때, 문제점은 호스트에서 맵과 리듀스를 한다면 데이터가 어떻게 분할됐는지 알 수 있지만, SSD에서는 이를 알 수 없음
    - 따라서 SSD 내부에서 Mapper에 의해 분할된 청크에 의해 데이터가 어떻게 분할됐는지 알 수 없음
- 해결방안
    - 호스트 컴퓨터에 위와 같은 문제를 해결하기 위해 정보를 받음
    - SSD에 랜선, 네트워크 카드를 넣어서 호스트 컴퓨터에 정보 직접 받아옴 

### Feature offloading
- 어떤 기능을 SSD 내부에서 처리할 것인지 결정하는 것이 중요함
    - 왜냐면 SSD 내부의 프로세서는 호스트 컴퓨터의 프로세서보다 성능이 떨어지기 때문
    - 따라서 Mapper는 SSD 내부에서 처리하고, Reducer는 호스트 컴퓨터에서 처리하도록 했음

### A pseudo fully distributed mode
    - 하둡은 오직 세가지의 모드만을 지원함
        - Standalone mode:
            - 하나의 컴퓨팅 노드에서 모든 작업을 처리함
        - Pseudo-distributed mode:
            - 하나의 컴퓨팅 노드에서 두개의 노드 (네임노드, 데이터노드)를 띄워서 작업을 처리함
        - Fully distributed mode:
            - 여러개의 컴퓨팅 노드에서 작업을 처리함
    - Pseudo fully distributed mode:
        - 하나의 컴퓨팅 노드에서 여러개의 프로세스 노드를 띄워서 작업을 처리함
        - 이 모드에서는 Mapper는 SSD 내부에서 처리하고, Reducer는 호스트 컴퓨터에서 처리함
![alt text](image-13.png)