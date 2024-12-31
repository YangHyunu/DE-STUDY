# SQL vs NoSql

-  SQL : vertical scalability
-  NoSql: horizental Scalability
   - > 수평적으로 확장(다수의 vm 혹은 노드)
   - **Scale out**: 여러 대의 컴퓨터를 활용해 성능을 향상시킴. 가성비 측면에서 유리하다.
   - 현대의 클라우드 컴퓨팅 환경 혹은 PC 들로 구성된 클러스터 컴퓨팅 환경에 매우 적합함

### Relational Database
- RDBMS는 수십 년 동안 지배적이었다.
  - 영구적인 데이터의 효과적이고 효율적인 관리
  - 표준 데이터 모델과 언어 (SQL)가 존재
    - 어떤 머신에서라도 공통된 언어로 RDBMS를 컨트롤 할 수 있다.
- `ACID` 속성:
  - Atomicity (원자성)
  - Consistency (일관성)
  - Isolation (고립성)
  - Durability (지속성)
- 동시성 제어
- 단일의 거대한 머신에서 실행되도록 설계됨

![alt text](image-51.png)
### RDBMS의 한계 및 문제점
 - RDBMS의 경우 데이터베이스의 테이블(스키마)는 `프로그래머`가 사용하는 데이터와 매우 다르게 정의되어 있는 경우가 많다. 즉, 한마디로 애플리케이션에서 사용되는 데이터 혹은 개발자가 사용하는 데이터의 구조와 데이터베이스의 데이터 `구조가 상이`한 문제
  
**관계형 데이터베이스 모델링**:

관계형 데이터베이스는 데이터를 테이블 형태로 저장하며, 각 테이블이 서로 다른 엔터티(Orders, Customers, Order Lines, Credit Cards)를 나타낸다.
데이터는 여러 `테이블`에 걸쳐 `분산`되어 있으며, 외래 키(Foreign Key)를 통해 연결됨. 이는 데이터 중복을 최소화하고 데이터 일관성을 높이는 장점이 있으나, 프로젝션을 위해서는 각 테이블을 `조인`해야 하는 번거로움이 있음

**애플리케이션 데이터 구조**:

애플리케이션에서 데이터는 종종 객체나 중첩된 구조로 표현된다. 예를 들어, 주문(Order)은 고객(Customer), 주문 항목(Order Lines), 결제 정보(Payment Details) 등 여러 정보를 `하나`의 `객체`에 포함할 수 있다.
이 `중첩된 구조`는 애플리케이션 개발자가 사용하는 방식으로, 데이터를 한 번에 처리하고 관리하기 쉽다.

**임피던스 불일치**:
![alt text](image.png)
- 관계형 데이터베이스의 `분리된` 테이블 `구조`와 애플리케이션의 `중첩된 객체 구조` 간의 차이로 인해 데이터 전송 및 변환 과정에서 복잡성이 발생. 
- 애플리케이션에서 데이터를 처리하려면 여러 테이블에서 데이터를 가져와서 다시 조인해야 하며, 이는 성능 저하와 복잡성을 유발할 수 있다.

#### 즉, RDBMS는 현대의 컴퓨팅 환경에 적합하지 않다.
- 한마디로 RDBMS의 장점인 ACID가 분산 컴퓨팅 환경에서는 단점으로 작용한다.
### A Shift from Scale Up to Scale Out

- 데이터 볼륨의 폭발적인 증가로 인해, 저가 하드웨어 클러스터 기반의 컴퓨터 아키텍처가 유일한 해결책으로 등장했다.
- 관계형 데이터베이스는 `클러스터에서 실행되도록 설계되지 않았으며`, 클러스터에서 잘 작동하지 않는다!
- 관계형 데이터베이스와 클러스터 간의 임피던스 불일치로 인해 일부 조직은 데이터 저장에 대한 대안 솔루션을 고려하게 되었다.
  - 예: Google의 BigTable, Amazon의 Dynamo

## NoSQL
 - 90년대 말 (인터넷이 급속도로 대중화되던 시기)
 - NoSQL이 무엇인지 명확한 정의가 존재하지 않는다.
 - 매우 큰 볼륨의 데이터를 저장하는데 적합하다.

### 주요 특징:
- SQL 및 관계형 모델을 사용하지 않음을 지향한다.
- 오픈 소스 프로젝트 (대부분)
- 클러스터에서 실행 (즉, 분산 처리)
- 스키마리스 (즉, 스키마가 없음)
- 간단한 API

| Category       | SQL                                                                                   | NoSQL                                                                                     |
|----------------|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Pros**       | - 구조화된 데이터와 트랜잭션에 적합함<br>- 높은 성능의 워크로드 지원<br>- 다양한 툴과 안정성이 입증됨 | - 비관계형 혹은 비정형  데이터에 적합<br>- 스키마가 없고 구조 수정과 데이터 변경이 쉬움<br>- 쉽게 확장 가능, 분산 시스템에 적합 |
| **Cons**       | - 확장 및 수정에 어려움이 있음<br>- 고정된 스키마로 데이터 조직                                      | - 설치 및 관리 툴이 미성숙<br>- 응답 속도가 느릴 수 있음-> 분산시스템이라 레이턴시가 존재                        |
| **Examples**   | MySQL, PostgreSQL, SQL Server, Oracle                                                | Amazon DynamoDB, MongoDB, Couchbase, Riak                                                 |

---
## NoSQL 데이터 모델링

### Data Model
- 데이터 모델이란 정보를 표현 및 저장하기 위한 구성요소의 집합
- **Relational model**: 테이블, 열, 행 -> "개념적"
- **Storage model**: DBMS가 데이터를 내부적으로 저장하고 조작하는 방식 -> "물리적"
- 데이터 모델은 일반적으로 Storage model과 `독립`적이다.

# NoSQL 시스템의 데이터 모델:
- **Aggregate models**
  - **Key-Value**
  - **Document**
  - **Column-family**
- **Graph-based models**

---

## 정리 !
  - RDBMS의 데이터 모델과 애플리케이션 혹은 개발자입장에서 다루는 데이터의 형태가 다르고 비 직관적이다.
  - 컴퓨팅 성능이 발전하면서 분산 컴퓨팅 성능이 높아짐에 따라 NoSQL 또한 크게 발전하게 되었다. -> 샤딩이 필요없고, 서로 관련있는 데이터를 하나의 단위로서 취급하므로 ,단위가 `여러 서버에 `**분산**될 수 있으며 모든 관련 데이터를 한 번에 불러올 수 있어 효율적이다.
  - Aggregate는 데이터를 묶어서 관리하므로 데이터 일관성을 유지하고, 클러스터 환경에서의 분산 처리 및 확장성을 용이하게 한다.
  
#### 정리 :
RDBMS에서 정의하는 데이터의 구조와 실제 애플리케이션에서 발생하고, 프로그래머가 다루게되는 데이터의 구조가 달라 문제가됨 임피던스 불일치, 이는 RDBMS가 ACID를 보장하기 위해 희생한 결과.
또한 RDBMS는 처음 만들어졌을 때 부터 하나의 단일 머신에서 작동하는것을 가정하고 설계되었고, 따라서 기존 RDBMS에서는 데이터 중복을 방지하기 위해 `샤딩`을 사용하여 데이터를 파편화된 상태로 저장했으나 , Aggregate는 이미 관련된 데이터의 집합이므로 샤딩이 필요 없다. 즉, 여러개의 작은 머신을 클러스터와 하여 작업하는 클러스터 컴퓨팅 환경에 한계를 가지고 있음. 반면 대부분의 NOSQL의 경우 오토샤딩을 기본적으로 지원하므로 Aggragate된 데이터를 여러 머신에서 처리할 수 있음.


---

### Aggregate의 정의
- 관련된 데이터의 모음으로, 이를 **하나의 단위**로 처리한다.
- 데이터베이스 내에서 ACID 작업(원자성, 일관성, 고립성, 지속성)의 `경계` 역할을 하며, 데이터 조작과 일관성 관리를 용이하게 한다.
- 즉 전체 데이터에 대한 ACID를 완벽하게 보장하지는 않지만 Aggregate된 데이터들 사이에는 `ACID를 보장`할 수 있다.

### Aggregate의 장점
- 애플리케이션 개발자가 데이터를 다루기 쉽다. 관련된 데이터를 묶어서 `하나의 단위`로 접근할 수 있기 때문이다.
- 데이터베이스 시스템이 클러스터 환경에서 데이터를 더 쉽게 관리할 수 있다.
- 이 `단위`가 여러 서버에 `분산`될 수 있으며 모든 관련 데이터를 한 번에 불러올 수 있어 효율적이다.
-  기존 RDBMS에서는 데이터 중복을 방지하기 위해 `샤딩`을 사용하여 데이터를 파편화된 상태로 저장했으나 , **Aggregate**는 이미 관련된 데이터의 집합이므로 샤딩이 필요 없다.
- Aggregate-oriented Data Model은 관련 데이터를 하나의 단위로 묶어 관리함으로써 데이터 일관성을 유지하고, 클러스터 환경에서의 분산 처리 및 확장성을 용이하게 한다.

<details>
<summary>토글: </summary>
<div markdown="1">
![alt text](image-127.png)
![alt text](image-53.png)
# Aggregate implementation
![alt text](image-55.png)
</div>
</details>

![alt text](image-54.png)


### Aggregate implementation
 - 연관된 데이터를 하나의 단위로 묶어서 함께 저장함. -> 사용자(Customer)의 관점에서 데이터를 Customer , Order를 큰 기준으로 `관련있는 데이터들의` 단위로 저장함.

##### Customer (고객):
```
{ "id": 1,
  "name": "Martin",
  "billingAddress": [{"city": "Chicago"}] }
```
##### Order (주문):
```
{
    "id": 99,
    "customerId": 1,
    "orderItems": [
        {
            "productId": 27,
            "price": 32.45,
            "productName": "NoSQL Distilled"
        }
    ],
    "shippingAddress": [{"city": "Chicago"}],
    "orderPayment": [
        {
            "ccinfo": "1000-1000-1000-1000",
            "txnId": "abel1f879rft",
            "billingAddress": {"city": "Chicago"}
        }
    ]
}
```
![alt text](image-59.png)
![alt text](image-60.png)
#### Aggregate implementation (2)
```
{
  "customer": {
    "id": 1,
    "name": "Martin",
    "billingAddress": [
      { "city": "Chicago" }
    ],
    "orders": [
      {
        "id": 99,
        "customerId": 1,
        "orderItems": [
          {
            "productId": 27,
            "price": 32.45,
            "productName": "NoSQL Distilled"
          }
        ],
        "shippingAddress": [
          { "city": "Chicago" }
        ],
        "orderPayment": [
          {
            "ccinfo": "1000-1000-1000-1000",
            "txnId": "abelif879rft",
            "billingAddress": { "city": "Chicago" }
          }
        ]
      }
    ]
  }
}

```
#### 구조 설명:
- Customer를 Key의 역할을 하여 Customer에 대한 모든 데이터를 저장한다.
- Customer 아래에 있는 모든 엔티티들(Order, Order Items, Order Payment, Address)은 Customer와 연관되어 있으며, Customer를 통해 접근하고 관리
- 마찬가지로 RDBMS의 데이터 모델링에 비해 훨씬 직관적이다.


#### Aggregate 경계 - Aggregate Boundaries

- Aggregate 경계를 정의하는 보편적인 방법은 없다.
- Aggregate 경계는 데이터를 어떻게 다루는지에 따라 결정된다.
- 예)
  - 한 번에 단일 주문에 대한 접근을 하는 경우: 첫 번째 구조.
  - 모든 주문을 포함한 고객 데이터 접근이 필요한 경우: 두 번째 구조.
- 즉 ,Context에 따라 경계를 설정해야 하며, 애플리케이션에 따라 선호하는 방식이 다를 수 있다.

#### 장점
- 클러스터 환경에서 유리하다.
- 데이터가 함께 조작되므로 동일한 노드에 위치해야 한다.

#### 단점
- Aggregate 구조는 일부 데이터 상호작용에 도움이 되지만, 다른 상호작용에는 방해가 될 수 있다. 즉, 경계를 정하기 모호한 경우
- 데이터 유효성 검증 및 보장을 하기 어렵다.
- Aggregate 간의 관계 처리가 더 어려워진다.
---
## Transaction? -> (ACID)

### Relational Databases
- 관계형 데이터베이스는 데이터 베이스에 있는 전체 데이터에 대한 ACID 트랜잭션을 지원한다.

### Aggregate-oriented Databases
- 여러 Aggregate에 걸친 ACID 트랜잭션을 지원하지 않는다.
- `하지만 , 단일 Aggregate의 ACID 트랜잭션을 지원한다.`
- 데이터를 어떻게 Aggregate할지 결정하는 고려 사항의 일부이다.

![alt text](image-1.png)


## K-V Store (Key-Value Store)

### Strongly Aggregate-oriented
- 데이터베이스에 많은 Aggregate를 갖는다.
- 각 Aggregate는 Key<primary_key역할>를 가진다.

### Data Model
- <key, value> 쌍의 집합
- Value: 한 Aggregate 인스턴스(즉 Aggregate된 데이터의 집합)
- Aggregate의 **구조**는 보이지 않는다.
  - 즉 , 데이터 간의 관계나 계층적인 구조를 **표현할 수 없다**.

- Value 데이터를 불가분의 `BLOB`으로 취급한다.
  - BLOB: Binary Large Object

### Access to an Aggregate
- 키를 기반으로 조회한다.
- 한마디로 키 값을 입력받으면 value를 반환한다. 즉, 데이터의 접근에 매우 간단한 구조
  - 다만 값을 통째로 저장하므로, 데이터의 일부분만 조회하거나 수정하는 것이 `불가능`하다.
- > key: Head를 던져주면 value: JSON 타입의 데이터 반환

## Principles

- 키-값 저장소에서는 값이 고유한 키에 매핑된다.
- 데이터를 저장하려면 키와 값을 모두 제공해야 한다: `store.put("user-1234", "...")`
- 값을 조회하려면 키를 제공해야 한다: `value = store.get("user-1234")`
- 키는 데이터베이스, 버킷, key-스페이스 등으로 조직된다.
- 값은 알려진 구조를 가지지 않으므로 키를 통해서만 조회할 수 있다.

### Basic Operations

- KV Store는 매우 간단하고 효율적인 연산을 제공한다:
  - `put` (또는 `set`), `get`, `del`, `replace`, `incr`, `decr`
- 자동 TTL<Time to live> 기반 값 만료를 제공한다.
  - 캐시에 사용된다.
    - ex 네이버 즐겨찾기 -> 데이터 센터에 접근할 필요도 없이 앞단에서 값을 리턴하여 리소스를 절약
- 일부는 전체 또는 제한된 키 목록을 검색하기 위한 Key-Enumerate를 제공한다.


![alt text](image-58.png)

![alt text](image-57.png)



## 2. Document database -> MongoDB

### Strongly Aggregate-oriented
- 많은 Aggregate를 포함한다.
- 각 Aggregate는 키를 가진다.

#### Data Model
- <key, document> 쌍의 집합
- Document: Aggregate 인스턴스
- Aggregate의 구조를 볼 수 있다.
- Aggregate에 넣을 수 있는 데이터에 제한이 있다.

#### Access to an Aggregate
- Aggregate 내 필드를 기반으로 `쿼리`한다.
  - 즉, 인스턴스 내부의 특정한 데이터에 각 각 접근 가능하다.
  
#### Principles
- **Documents**는 독립적인 Aggregate 데이터 구조이다.
- 속성(name-value 쌍)으로 구성된다.
- 속성 값은 데이터 타입을 가지며, 중첩되거나 계층적일 수 있다.
- Document 저장소는 타입 시스템을 가지고 있어 기본적인 데이터 유효성 검사를 수행할 수 있다.
- 각 Document는 암묵적인 스키마를 가지며, Document 저장소는 모든 Document 속성과 하위 속성에 개별적으로 접근할 수 있다.
- 많은 쿼리 기능을 제공한다.
### Data Accessses in document store
- Document 내부를 쿼리할 수 있다:
  - 예: "Refactoring Databases 제품을 포함하는 모든 주문을 찾아라"
- Customer 객체에서 Orders에 대한 참조를 제거할 수 있다.
- Customer가 새로운 주문을 할 때마다 Customer 객체를 업데이트할 필요가 없다.
```
{
  "customer": {
    "customerId": 1,
    "name": "Martin",
    "billingAddress": [
      {
        "city": "Chicago"
      }
    ],
    "payment": [
      {
        "type": "debit",
        "ccinfo": "1000-1000-1000-1000"
      }
    ]
  },
  "order": {
    "orderId": 99,
    "customerId": 1,
    "orderDate": "Nov-20-2011",
    "orderItems": [
      {
        "productId": 27,
        "price": 32.45
      }
    ],
    "orderPayment": [
      {
        "ccinfo": "1000-1000-1000-1000",
        "txnId": "abelif879rft"
      }
    ],
    "shippingAddress": {
      "city": "Chicago"
    }
  }
}

```

![alt text](image-61.png)


## Key-Value Database vs. Document Database

### Key-Value Database
- 구조: 키 + 큰 BLOB(Binary Large Object)로 이루어지며, 대부분 의미 없는 데이터 비트들이 포함된다.
- 유연성: 키와 연결된 데이터는 어떤 형식이든 저장할 수 있다.
- 접근 방식: 오직 키를 통해서만 집합(aggregate)에 접근할 수 있다. 내부 구조에 대해 특정 필드를 기준으로 조회할 수는 없다.

### Document Database
- 구조: 키 + 구조화된 집합(aggregate)으로 이루어진다.
- 유연성: 데이터 접근의 유연성이 더 높다.
  - 쿼리 기능: 집합 내 필드를 기반으로 데이터베이스에 쿼리를 제출할 수 있다.
  - 부분 조회: 전체 집합이 아닌, 집합의 특정 부분만 조회할 수 있다.

### 요약
- Key-Value Database는 단순히 키와 연결된 데이터 덩어리를 저장하는 방식으로, 내부 구조에 대한 조회 기능이 없다.
- Document Database는 구조화된 데이터를 저장하며, 내부 `필드`를 기준으로 쿼리하거나 집합의 일부만 조회하는 등 더 유연한 접근 방식을 제공한다.


# Column(-Family)Stores

![alt text](이미지/image-62.png)

- 많은 aggregate를 저장할 수 있음
- 데이터를 row<record>형태로 저장하는게 아닌 **column wise**로 저장함
- row 형태로 데이터를 조회하면 필요하지 않은 칼럼의 데이터까지 같이 조회됨
- 예 -> University Table에서 student테이블을 이용해서 학생 이름과 성적을 조회화고 싶을 때, 학생 이름과 성적만 조회하는 쿼리를 수행하는경우 전체 테이블을 불러온 후 학생 이름과 성적을 사영시키는 방식으로 작동하지만, column Store의 경우 필요한 칼럼 학생 이름, 성적 만 불러올 수 있음.

- 자주 함께 접근(Access)되는 칼럼들을 묶어 놓은것을 `Column-Family`라고 함.
![alt text](image-2.png)
**row-store**
- 레코드 형태로 저장되므로 입력하고 수정하기 쉬움
- (OLTP)트랜잭션 처리에 적합함.
- 레코드 전체를 저장하고 읽으므로 불필요한 `리소스낭비`가 발생함
  - 빅데이터시대에 부적합함

**column-store**
- Column Store는 `데이터를 빠르게 읽어올 수 있음`
- 오직 `관련있는` 데이터만 읽어올 수 있음
- 즉, 데이터 조회 및 분석에 적합함(OLAP)
- 단점: 만약 row(레코드)형식으로 데이터를 저장해야 할때는 칼럼형태로 여러번 저장하여야 함.
---
## Properties of Column-Store

### Operations
- 특정 칼럼을 선택하는 연산을 허용한다.
  - 예: `get('1234', 'name')`

### Each Column
- 단일 컬럼 패밀리의 일부여야 한다.
- 접근의 `단위`로 작동한다.
- 어떤 컬럼이든지 어떤 행에 추가할 수 있다.(대신 한 횡을 채우기 위해서는 여러번 추가해야 함..)

### Two Ways to Look at Data
- **Row-oriented**:
  - 각 행은 하나의 집합이다.
  - 컬럼 패밀리는 그 집합 내에서 유용한 데이터 Aggregate를 나타낸다.

- **Column-oriented**:
  - 각 컬럼 패밀리는 레코드 타입을 정의한다.
  - 모든 컬럼 패밀리의 레코드를 조인한 것이 행이다.


![alt text](image-64.png)

![alt text](image-65.png)

# 그래프 db

### Motivation

- **Frustration with Relational Databases**:
  - 복잡한 관계는 복잡한 조인을 필요로 한다.

- **Goal**:
  - 복잡한 관계를 포함하는 데이터를 효과적으로 캡처한다.
  - 데이터를 그래프 형태로 자연스럽게 모델링한다.

- **Use Cases**:
  - **Highly Connected Data**:
    - 예: 소셜 네트워크
  - **Location-Based Services**:
    - 예: 배달 경로 계획
  - **Recommendation Systems**:
    - 예: 자주 방문한 명소, 구매한 제품

![alt text](image-66.png)
- 서로 다른 테이블에 있는 데이터간의 관계를 보여주기 위해 기존 RDBMS에서는 많은 조인연산이 필요함 즉, 엄청난 오버헤드를 발생시킴

- sns , 네비게이션 시스템
![alt text](image-67.png)
- Possible query: “find the books in the Databases category that are
written by someone whom a friend of mine likes”

