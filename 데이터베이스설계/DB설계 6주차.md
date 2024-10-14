# DB 설계 6주차

## Joined Relations
조인 연산 (Join Operations)
두 개의 관계를 결합하여 새로운 릴레이션을 반환한다.
조인 연산은 두 관계 간의 데이터를 __카테시안 곱__ 한 후, 특정 조건에 따라 해당 조건에 맞는 튜플(행)을 반환하며, 반환될 속성들을 지정할 수 있다.
세 가지 주요 조인 방식이 존재
1. Natural Join (자연 조인)
두 테이블의 `공통 속성`을 기준으로 자동으로 조인.
조건 없이 `동일한 이름`을 가진 속성을 기준으로 자동 매칭.
공통 속성을 가진 두 테이블 간의 중복 컬럼이 제거됨.
2. Inner Join (내부 조인)
두 테이블에서 `일치하는 값을 가진 행만 반환`합니다.
즉, 조건을 만족하는 행들만 결합하여 결과를 생성
3. Outer Join (외부 조인)
`일치하지 않는 값도 포함하는 조인`



## Natural Join 

### Natural Join을 사용한 다중 관계 결합

`FROM` 절에서 여러 관계를 **Natural Join**으로 동시에 결합할 수 있다:

```sql
SELECT A₁, A₂, ... Aₙ
FROM r₁ NATURAL JOIN r₂ NATURAL JOIN ... NATURAL JOIN rₙ
WHERE P;
```
- r₁, r₂, ... rₙ: 조인할 테이블(관계).
- A₁, A₂, ... Aₙ: 선택할 컬럼들.
- P: 조건문(옵션).

### `Dangerous in Natural Join`
- Beware of unrelated attributes with same name which get equated incorrectly
- Example -- List the names of students along with the titles of courses
that they have taken

#### Corret query <정상>
```
SELECT name, title
FROM student NATURAL JOIN takes, course
WHERE takes.course_id = course.course_id;
```
1. student 테이블과 takes를 카다시안 곱을 한 후 course_id에 대해서도 카다시안 곱을 실행 => 그 중 WHERE 절의 조건을 만족하는 튜플만 반환!
2. **중요**
- NATURAL JOIN은 `공통 속성`을 자동으로 매칭하므로 우선적으로 student 와 takes 테이블 간의 `공통속성(ID)를 기준`으로 조인됨 
- 이후 `course_id`를 기준으로 course 테이블과 takes테이블이 명시적으로 조인되어
- 모든 학생의 이름과 해당 학생이 수강한 강좌의 제목을 반환함.
#### Incorect query
``` 
SELECT name, title
FROM student NATURAL JOIN takes NATURAL JOIN course;
```
- 세 테이블 모두 동일한 attribute(속성)을 가지고 있지만 속성의 의미<정보>가 다르다.
- `NATURAL JOIN`은 공통 속성을 기준으로 자동으로 조인되기 때문에, 여기서 `모든 테이블에서 공통`되는 속성을 찾아서 조인하게 된다.
- 여기서 문제점은 course 테이블과 student 테이블 간에 `공통 속성을 갖지 않는 경우가 있을 수도 있다는것!`
- 즉, 학생이 만약 다른 학과의 강좌를 수강한 경우 이를 누락한 쿼리를 반환할 수 있다.

## Natural join with Using Clause
```
SELECT name, title
FROM (student natural join takes) join course using(course_id);
```
Using 절을 사용하면서 명시적으로 속성을 지정하면서 위와 같은 잘못된 쿼리를 방지할 수 있음.

## Join condition

```
SELECT *
FROM student join takes on student.ID = takes.ID
```
같은 쿼리
```
SELECT *
FROM student, takes
WHERE student.ID = takes.ID; 
```
Using을 사용한 같은 쿼리
```
SELECT *
FROM student join takes 
USING (ID);
```

## Outer Join
![image](https://github.com/user-attachments/assets/3ca58066-3de5-405d-9c73-d26ced435cee)


Outer Join은 조인 연산의 확장으로, 정보 손실을 방지하는 방식.
- 일반적인 조인은 두 테이블 간의 일치하는 데이터를 결합하지만, Outer Join은 일치하지 않는 데이터도 결과에 포함되도록 함.

 - Outer Join은 조인을 수행한 후, `다른 relation`에 일치하지 않는 튜플(행)을 결과에 추가.
        즉, 한쪽 테이블에만 존재하는 행도 null로 채워진 후 결과에 포함됨.
.

    Outer Join의 세 가지 형태:
        `Left Outer Join`: 왼쪽 테이블의 모든 행을 유지하고, 오른쪽 테이블에서 일치하지 않는 값은 null로 반환.
        `Right Outer Join`: 오른쪽 테이블의 모든 행을 유지하고, 왼쪽 테이블에서 일치하지 않는 값은 null로 반환.
        `Full Outer Join`: 양쪽 테이블의 모든 행을 유지하며, 일치하지 않는 행은 null로 반환.

#### 요약:
Outer Join은 테이블 간의 일치하는 데이터뿐만 아니라, 한쪽 테이블에만 존재하는 데이터도 포함하여 조인을 수행하는 방식으로, Left, Right, Full Outer Join은 각각 다르게 작동하며, 조인되지 않는 데이터는 null 값을 통해 표시된다.



## Joined Types and Conditions

![image](https://github.com/user-attachments/assets/23d5d78e-b5d7-4e98-b082-915f97a67320)





## View
### View Definition
![image](https://github.com/user-attachments/assets/7dd7bbc5-0bbb-4d15-8ec8-56cdb75d115f)

### View Defined Using Other Views
![image](https://github.com/user-attachments/assets/f8838fe0-b101-4585-84d3-a1c8997792f2)


```

```

## View Expansion

- 다른 뷰를 사용하여 정의된 뷰의 의미를 정의하는 방법.
- 뷰 `v₁`이 표현식 `e₁`에 의해 정의된다고 가정하면, 이 표현식 `e₁`은 뷰 관계를 포함할 수 있다.

- ```repeat```
Find any view relation vi in e1
Replace the view relation vi by the expression defining vi
- `until` no more view relations are present in e1

![image](https://github.com/user-attachments/assets/b784cbaa-f3e4-4c68-82ed-4e7de7b05bf7)


## Update of View

- 사전에 만든 view에 새로운 튜플 넣기
```
INSERT INTO faculty
values ('30765', 'Green', 'Music);
```
- `유의점 1`
    - faculty view가 기본적으로 instructor relation에 `기반`하므로 해당 relation에 DDL로 정해진 조건이나 속성의 도메인에 속하는 값을 넣어야 함.

- `유의점 2`
    - view의 Update가 성공한다면, 그 내용이 view뿐만 아니라 기반인 relation에도 반영된다.

문제 해결 방법:
1. 삽입을 거부하는 방법
2. 튜플에 null값을 지정하는 방법
```
('30765', 'Green', 'Music', null)
```
### Some Updates Cannot be Translated Uniquely
![image](https://github.com/user-attachments/assets/5ff87de4-42a9-47b7-a48c-992da5ea5cad)

```
create view instructor_info as
select ID, name, building
from instructor, department
where instructor.dept_name = department.dept_name;
```
- View에 새로운 내용을 반영하려고 할때
```
INSERT INTO instructor_info
VALUES ('69987', 'White', 'Taylor');
```
- Issues
    - Which department, if multiple departments in Taylor?
        - department.dept_name을 알 수 없는 상황에서 building = 'Taylor'라는 조건만으로는 어느 부서에 속하는지 결정할 수 없다.

    - What if no department is in Taylor?
        - 만약 'Taylor'라는 건물에 부서가 없다면 삽입된 데이터가 어떻게 처리 되는지? 

- `요약`:

    - 이 예시는 뷰를 통해 데이터를 삽입할 때, 뷰가 참조하는 원본 테이블에서 여러 가지 `애매한 상황`이 발생할 수 있음을 보여줌.
    -  특히, 뷰가 여러 테이블을 결합하고 있을 때, 삽입된 데이터가 어느 테이블의 어떤 값을 `참조`하는지 `명확하지 않은 경우`가 있을 수 있으며, 이로 인해 업데이트가 고유하게 번역될 수 없는 문제가 발생함을 고려해야 함.

### And Some Not at All
우선 instructor 릴레이션에서 History 부서에 속하는 모든 강사의 정보를 포함하는 view를 작성했다.
```
CREATE VIEW history_instructor  as
SELECT *
FROM instructor
WHERE dept_name = 'History';
```
만약 이때, view에 History부서가 아닌 다른 부서의 정보를 입력한다면?
```
INSERT INTO history_instructor 
VALUES ('25566', 'Brown', 'Biology', 100000);
```
쿼리가 정상적으로 실행되지 않을것이라 생각했으나, 정상적으로 쿼리가 실행됐다. 이유는 instructor 릴레이션에 제약조건이 없기 때문, 즉 다른 부서의 강사의 정보가 부적절하게 릴레이션에 반영될 수 있으므로 주의가 필요 !

- `해결방법`:
WITH CHECK OPTION 사용
```
CREATE VIEW history_instructors AS
SELECT *
FROM instructor
WHERE dept_name = 'History'
WITH CHECK OPTION;
```
WITH CHECK OPTION을 사용하여 VIEW를 업데이트 할때 
VIEW 안의 WHERE절의 조건문을 확인함.

## SQL에서 뷰 업데이트 규칙:

1. 대부분의 SQL 구현에서는 간단한 뷰에서만 업데이트를 허용한다. 
    - 즉, 복잡한 뷰나 여러 테이블을 참조하는 뷰에서는 업데이트가 불가능할 수 있다.

2. FROM 절에는 하나의 데이터베이스 관계만 있어야한다.
    -  즉, 뷰가 한 테이블만 참조할 때 업데이트가 가능. 여러 테이블을 조인하거나 결합한 뷰에서는 업데이트가 제한될 수 있다.

3. SELECT 절에는 관계의 속성 이름만 포함되어야 하며, 표현식, 집계 함수 또는 DISTINCT 지정이 없어야 한다.
    -   뷰에서 계산된 값이나 집계된 값이 있을 경우, 그 값을 수정할 수 없기 때문에 업데이트가 허용되지 않는다.

4. SELECT 절에 포함되지 않은 속성은 NULL로 설정될 수 있다.
    -   만약 뷰에 포함되지 않은 속성에 대한 값이 없으면, 해당 속성의 값은 NULL로 설정됨.

5. 쿼리에는 GROUP BY 또는 HAVING 절이 없어야 한다.
    -   앞에서 말한것 처럼 그룹화나 필터링이 있는 뷰는 업데이트할 수 없다. 
    - 이는 뷰가 복잡한 집합 연산을 포함하지 않아야 한다는 의미.

`요약`:

1. SQL에서 뷰를 업데이트하려면 뷰가 단순해야 하며, 여러 테이블을 참조하거나 복잡한 연산이 포함된 경우에는 업데이트가 불가능.
2. 제한 조건을 만족하는 단순한 뷰에서만 데이터를 삽입하거나 수정할 수 있다.

Outer Join은 조인 연산의 확장으로, 정보 손실을 방지하는 방식.
- 일반적인 조인은 두 테이블 간의 일치하는 데이터를 결합하지만, Outer Join은 일치하지 않는 데이터도 결과에 포함되도록 함.

 - Outer Join은 조인을 수행한 후, `다른 relation`에 일치하지 않는 튜플(행)을 결과에 추가.
        즉, 한쪽 테이블에만 존재하는 행도 null로 채워진 후 결과에 포함됨.
.

    Outer Join의 세 가지 형태:
        `Left Outer Join`: 왼쪽 테이블의 모든 행을 유지하고, 오른쪽 테이블에서 일치하지 않는 값은 null로 반환.
        `Right Outer Join`: 오른쪽 테이블의 모든 행을 유지하고, 왼쪽 테이블에서 일치하지 않는 값은 null로 반환.
        `Full Outer Join`: 양쪽 테이블의 모든 행을 유지하며, 일치하지 않는 행은 null로 반환.

#### 요약:
Outer Join은 테이블 간의 일치하는 데이터뿐만 아니라, 한쪽 테이블에만 존재하는 데이터도 포함하여 조인을 수행하는 방식으로, Left, Right, Full Outer Join은 각각 다르게 작동하며, 조인되지 않는 데이터는 null 값을 통해 표시된다.



## Joined Types and Conditions

![alt text](image-11.png)




## View

![alt text](image-15.png)

![alt text](image-12.png)

```

```

## View Expansion

- 다른 뷰를 사용하여 정의된 뷰의 의미를 정의하는 방법.
- 뷰 `v₁`이 표현식 `e₁`에 의해 정의된다고 가정하면, 이 표현식 `e₁`은 뷰 관계를 포함할 수 있다.

- ```repeat```
Find any view relation vi in e1
Replace the view relation vi by the expression defining vi
- `until` no more view relations are present in e1

![alt text](image-13.png)

## Update of View

- 사전에 만든 view에 새로운 튜플 넣기
```
INSERT INTO faculty
values ('30765', 'Green', 'Music);
```
- `유의점 1`
    - faculty view가 기본적으로 instructor relation에 `기반`하므로 해당 relation에 DDL로 정해진 조건이나 속성의 도메인에 속하는 값을 넣어야 함.

- `유의점 2`
    - view의 Update가 성공한다면, 그 내용이 view뿐만 아니라 기반인 relation에도 반영된다.

문제 해결 방법:
1. 삽입을 거부하는 방법
2. 튜플에 null값을 지정하는 방법
```
('30765', 'Green', 'Music', null)
```
### Some Updates Cannot be Translated Uniquely
![alt text](image-14.png)
```
create view instructor_info as
select ID, name, building
from instructor, department
where instructor.dept_name = department.dept_name;
```
- View에 새로운 내용을 반영하려고 할때
```
INSERT INTO instructor_info
VALUES ('69987', 'White', 'Taylor');
```
- Issues
    - Which department, if multiple departments in Taylor?
        - department.dept_name을 알 수 없는 상황에서 building = 'Taylor'라는 조건만으로는 어느 부서에 속하는지 결정할 수 없다.

    - What if no department is in Taylor?
        - 만약 'Taylor'라는 건물에 부서가 없다면 삽입된 데이터가 어떻게 처리 되는지? 

- `요약`:

    - 이 예시는 뷰를 통해 데이터를 삽입할 때, 뷰가 참조하는 원본 테이블에서 여러 가지 `애매한 상황`이 발생할 수 있음을 보여줌.
    -  특히, 뷰가 여러 테이블을 결합하고 있을 때, 삽입된 데이터가 어느 테이블의 어떤 값을 `참조`하는지 `명확하지 않은 경우`가 있을 수 있으며, 이로 인해 업데이트가 고유하게 번역될 수 없는 문제가 발생함을 고려해야 함.

### And Some Not at All
우선 instructor 릴레이션에서 History 부서에 속하는 모든 강사의 정보를 포함하는 view를 작성했다.
```
CREATE VIEW history_instructor  as
SELECT *
FROM instructor
WHERE dept_name = 'History';
```
만약 이때, view에 History부서가 아닌 다른 부서의 정보를 입력한다면?
```
INSERT INTO history_instructor 
VALUES ('25566', 'Brown', 'Biology', 100000);
```
쿼리가 정상적으로 실행되지 않을것이라 생각했으나, 정상적으로 쿼리가 실행됐다. 이유는 instructor 릴레이션에 제약조건이 없기 때문, 즉 다른 부서의 강사의 정보가 부적절하게 릴레이션에 반영될 수 있으므로 주의가 필요 !

- `해결방법`:
WITH CHECK OPTION 사용
```
CREATE VIEW history_instructors AS
SELECT *
FROM instructor
WHERE dept_name = 'History'
WITH CHECK OPTION;
```
WITH CHECK OPTION을 사용하여 VIEW를 업데이트 할때 
VIEW 안의 WHERE절의 조건문을 확인함.

## SQL에서 뷰 업데이트 규칙:

1. 대부분의 SQL 구현에서는 간단한 뷰에서만 업데이트를 허용한다. 
    - 즉, 복잡한 뷰나 여러 테이블을 참조하는 뷰에서는 업데이트가 불가능할 수 있다.

2. FROM 절에는 하나의 데이터베이스 관계만 있어야한다.
    -  즉, 뷰가 한 테이블만 참조할 때 업데이트가 가능. 여러 테이블을 조인하거나 결합한 뷰에서는 업데이트가 제한될 수 있다.

3. SELECT 절에는 관계의 속성 이름만 포함되어야 하며, 표현식, 집계 함수 또는 DISTINCT 지정이 없어야 한다.
    -   뷰에서 계산된 값이나 집계된 값이 있을 경우, 그 값을 수정할 수 없기 때문에 업데이트가 허용되지 않는다.

4. SELECT 절에 포함되지 않은 속성은 NULL로 설정될 수 있다.
    -   만약 뷰에 포함되지 않은 속성에 대한 값이 없으면, 해당 속성의 값은 NULL로 설정됨.

5. 쿼리에는 GROUP BY 또는 HAVING 절이 없어야 한다.
    -   앞에서 말한것 처럼 그룹화나 필터링이 있는 뷰는 업데이트할 수 없다. 
    - 이는 뷰가 복잡한 집합 연산을 포함하지 않아야 한다는 의미.

`요약`:

1. SQL에서 뷰를 업데이트하려면 뷰가 단순해야 하며, 여러 테이블을 참조하거나 복잡한 연산이 포함된 경우에는 업데이트가 불가능.
2. 제한 조건을 만족하는 단순한 뷰에서만 데이터를 삽입하거나 수정할 수 있다.
