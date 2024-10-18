#### a)
```
SELECT DISTINCT student.ID , student.name
FROM student 
JOIN takes ON student.ID = takes.ID
JOIN course ON takes.course_id = course.course_id
WHERE course.dept_name = 'Comp. Sci.';
```
| id | name |
| :--- | :--- |
| 00128 | Zhang |
| 12345 | Shankar |
| 45678 | Levy |
| 54321 | Williams |
| 76543 | Brown |
| 98765 | Bourikas |

#### b)
```
SELECT student.ID, student.name
FROM student
WHERE NOT EXISTS (
    SELECT 1
    FROM takes
    JOIN section ON takes.course_id = section.course_id
    WHERE section.year < 2017
);
```
| id | name |
| :--- | :--- |
| 00128 | Zhang |
| 12345 | Shankar |
| 19991 | Brandt |
| 23121 | Chavez |
| 44553 | Peltier |
| 45678 | Levy |
| 54321 | Williams |
| 55739 | Sanchez |
| 70557 | Snow |
| 76543 | Brown |
| 76653 | Aoi |
| 98765 | Bourikas |
| 98988 | Tanaka |

#### c)
```
WITH max_sal AS(
    SELECT dept_name, max(salary) AS max_salary
    FROM instructor
    GROUP BY dept_name
)

SELECT instructor.dept_name ,salary
FROM instructor JOIN max_sal ON instructor.dept_name = max_sal.dept_name
WHERE instructor.salary = max_sal.max_salary;
```
| dept\_name | salary |
| :--- | :--- |
| Finance | 90000.00 |
| Music | 40000.00 |
| Physics | 95000.00 |
| History | 62000.00 |
| Comp. Sci. | 92000.00 |
| Elec. Eng. | 80000.00 |
| Biology | 100000.00 |

```
SELECT name , dept_name , salary
FROM instructor
WHERE (dept_name,salary) IN (SELECT dept_name,max(salary) as salary
                 FROM instructor
                 GROUP BY dept_name);
```
##### 주의: 
여기서 (dept_name,salary) 로 안하면 만약 연봉이 다른 부서의최고 연봉과 같은 경우에도 결과를 반환해서
잘못된 쿼리임 

#### d)
```
WITH max_sal AS (
    SELECT dept_name, max(salary) AS max_salary
    FROM instructor
    GROUP BY dept_name
)
SELECT MIN(max_salary) AS lowest_max_salary
FROM max_sal;
```
| lowest\_max\_salary |
| :--- |
| 40000 |

