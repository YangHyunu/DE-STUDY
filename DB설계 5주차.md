# DB 설계 5주차

## Aggregate Fn example;
- Find the avg salary of instructors in the Comp.Sci.
```
SELECT avg(salary) 
FROM instructor
WHERE dept_name = 'Comp. Sci.';
```
![alt text](image-1.png)

- Find the all number of tuple in the course relation
```
SELECT COUNT(*)
FROM course;
```

### 주의해야 할 점 !
- 에러가 나는 쿼리 !
```
/*erroneous query*/
SELECT dept_name , ID , avg(salary)
from instructor
GROUP BY dept_name;
```
- aggregate fn 외부에서 SELECT 된 attribute는 반드시 GROUP BY절 내에 위치해 있어야 한다. , 만약 GROUP BY 절이 리턴한 릴레이션에 해당 attribute가 없으면 오류가 발생함.

### Having Clause
- Find the name and ..
```
SELECT name , avg(salary) as avg_salary
FROM instructor
GROUP BY dept_name
HAVING avg(salary)>42000;
```
- 유의 해야 할 점은 Having절의 쿼리는 GROUP BY가 이루어 진 후에 실행이 된다는 점으로, Where의 경우 GROUP BY 이전에 쿼리가 실행이 되서 같이 사용할 수 없음
![alt text](image-2.png)


# 중첩 서브쿼리 (Nested Subqueries)

- SQL에서 서브쿼리를 쿼리 안에 중첩해서 사용할 수 있다. 서브쿼리는 **SELECT-FROM-WHERE** 문 안에 들어가는 또 다른 쿼리라고 간주.

## 중첩하는 방법
- **EX**
```sql
SELECT A1, A2, ..., An
FROM r1, r2, ..., rm
WHERE P
```
- From 절: r1 같은 릴레이션 인스턴스 자리에 서브쿼리를 넣을 수 있다.
- Where 절: P 부분은 B <operation> (서브쿼리) 이런 형태로 서브쿼리와 함께 쓸 수 있고, B는 컬럼(속성)이고, operation은 연산자라고 보면 됨.
- Select 절: A1 자리에 서브쿼리를 넣어서 단일 값을 반환하게 만들 수도 있다.

## SET MEMBER SHIP
- Find courses offered in Fall 2017 and in Spring 2018

```
SELECT DISTINCT(course_id)
FROM section
WHERE semester = 'Fall' AND year = 2017
    AND course_id IN (
        SELECT course_id
        FROM section
        WHERE semester = 'Spring' AND year = 2018
    );
``` 
- WHERE 절에서 서브쿼리를 이용했음
![alt text](image-3.png)

```
SELECT DISTINCT(course_id)
FROM section
WHERE semester = 'Fall' AND year = 2017
    AND course_id NOT IN (
        SELECT course_id
        FROM section
        WHERE semester = 'Spring' AND year = 2018
    );
``` 

![alt text](image-4.png)

- Find the total # of unique student who have taken course sections taught by the instructor with ID 10101

```
SELECT COUNT(DISTINCT(ID))
FROM takes
WHWERE (course_id, sec_id, semester, year) in(
    SELECT course_id, sec_id, semester, year
    FROM teaches
    WHERE ID = 10101
    ;
)
```

## Set Comparision -"Some" Clauses => ANY와 같다.
![alt text](image-5.png)
- Find names of instructors with salary greater than that
of some (at least one) instructor in the Biology
department.

```
SELECT name
FROM instructor as S
WHERE S.salary > (SELECT MIN(salary) as salary
    FROM instructor as T
    WHERE dept_name = 'Biology');
```
or 밑의 쿼리에서는 DISTINCT()를 사용했는데 이유는 
- DISTINCT를 사용하지 않으면 중복 비교되어 연봉이 높은 강사? 교수가 계속 출력될 수 있으므로
```
SELECT DISTINCT(S.name)
FROM instructor as S , instructor as T
WHERE S.salary > T.salary AND T.dept_name = 'Biology'
```
SOME 을 이용한 쿼리
```
SELECT name
FROM instructor
where salary> ANY<SOME>(SELECT salary
    FROM instructor
    WHERE dept_name = 'Biology');
```
## Set Comparision -"ALL" Clauses 
![alt text](image-6.png)
#### 중요한 점은 ALL의 경우 모든 조건을 만족해야만 True값을 리턴한다는 점!
- Find the names of all instructors whose salary is greater than the salary of all
instructors in the Biology department

```
SELECT name
FROM instructor
WHERE salary > ALL (
    SELECT salary
    FROM instructor
    WHERE dept_name = 'Biology'
);
```
## Test for Empty Relations
![alt text](image-7.png)
#### 만약 서브쿼리가 비어있지 않은경우 (값을 리턴한 경우) True를 반환함 반대는 False
- EXIST 를 사용해서 - Find all courses offered in Fall 2017 and in Spring 2018 를 찾는 다른 방법

```
SELECT course_id
FROM section AS S
WHERE semester = 'Fall' AND year = 2017
AND EXISTS (
    SELECT *
    FROM section AS F
    WHERE semester = 'Spring' AND year = 2018
    AND S.course_id = F.course_id
);
```
### Use of “not exists” Clause 어려움....
- Find all students who have taken all courses offered in the Biology department.


```
SELECT DISTINCT(ID)
FROM takes
WHERE course_id = ALL (
    SELECT course_id
    FROM course
    WHERE dept_name = 'Biology');

```


## From 절에서 사용하는 서브쿼리
- Find the average instructors’ salaries of those departments where the average
salary is greater than $42,000.”
```
SELECT dept_name , avg_salary
FROM (
    SELECT dept_name, avg(salary) as avg_salary
    FROM instructor
    GROUP BY dept_name
    HAVING avg(salary)>42000
);
```
같은 쿼리
```
SELECT dept_name , avg_salary
FROM (
    SELECT dept_name, avg(salary) as avg_salary
    FROM instructor
    GROUP BY dept_name
)
WHERE avg_salary >42000;
```

```
SELECT dept_name, avg_salary
FROM (
    SELECT dept_name, AVG(salary)
    FROM instructor
    GROUP BY dept_name
) AS dept_avg (dept_name, avg_salary)
WHERE avg_salary > 42000;

```

## With Clause






## Scalar Subquery
- Scalar subquery 는 쿼리가 단일값을 반환할 것을 가정하고 사용한다.
- 예를 들어 department 테이블에 해당 department에 속하는 instructor의 수를 추가


## Modification of DB

- Dele