# Introduction to SQL
## Practice Exercises

##### 3.1 Write the following queries in SQL, using the university schema.
(We suggest you actually run these queries on a database, using the sample data that we provide on the website of the book, db-book.com. Instructions for setting up a database, and loading sample data, are provided on the above website.)

    a. Find the titles of courses in the Comp. Sci. department that have 3 credits.

    b. Find the IDs of all students who were taught by an instructor named Einstein; make sure there are no duplicates in the result.

    c. Find the highest salary of any instructor.

    d. Find all instructors earning the highest salary (there may be more than one with the same salary).

    e. Find the enrollment of each section that was offered in Fall 2017.

    f. Find the maximum enrollment, across all sections, in Fall 2017.

    g. Find the sections that had the maximum enrollment in Fall 2017.

##### 3.2 Suppose you are given a relation grade_points(grade, points) that provides a conversion from letter grades in the takes relation to numeric scores; for example, an "A" grade could be specified to correspond to 4 points, an "A-" to 3.7 points, a "B+" to 3.3 points, a "B" to 3 points, and so on. The grade points earned by a student for a course offering (section) is defined as the number of credits for the course multiplied by the numeric points for the grade that the student received. Given the preceding relation, and our university schema, write each of the following queries in SQL. You may assume for simplicity that no takes tuple has the null value for grade.

    a. Find the total grade points earned by the student with ID '12345', across all courses taken by the student.

    b. Find the grade point average (GPA) for the above student, that is, the total grade points divided by the total credits for the associated courses.

    c. Find the ID and the grade-point average of each student.

    d. Now reconsider your answers to the earlier parts of this exercise under the assumption that some grades might be null. Explain whether your solutions still work and, if not, provide versions that handle nulls properly.

##### 3.3 Write the following inserts, deletes, or updates in SQL, using the university schema.

    a. Increase the salary of each instructor in the Comp. Sci. department by 10%.
    ```
    UPDATE instructor
    SET salary = salary * 1.1
    WHERE dept_name = 'Comp. Sci.';
    ```

    b. Delete all courses that have never been offered (i.e., do not occur in the section relation).
    ```
    DELETE FROM course
    WHERE course_id IN (
    SELECT course.course_id
    FROM course LEFT JOIN section ON course.course_id = section.course_id
    WHERE section.course_id IS NULL
    );
    ```

    ```
    DELETE FROM course
    WHERE NOT EXISTS (
    SELECT 1
    FROM section
    WHERE section.course_id = course.course_id
    );
    ```
    c. Insert every student whose tot_cred attribute is greater than 100 as an instructor in the same department, with a salary of $10,000.

##### 3.4 Consider the insurance database of Figure 3.17, where the primary keys are underlined. Construct the following SQL queries for this relational database.

    a. Find the total number of people who owned cars that were involved in accidents in 2017.

    b. Delete all year-2010 cars belonging to the person whose ID is '12345'.

##### 3.5 Suppose that we have a relation marks(ID, score) and we wish to assign grades to students based on the score as follows: grade F if score < 40, grade C if 40 ≤ score < 60, grade B if 60 ≤ score < 80, and grade A if 80 ≤ score. Write SQL queries to do the following:

    a. Display the grade for each student, based on the marks relation.

    b. Find the number of students with each grade.

###### 3.6 The SQL LIKE operator is case sensitive (in most systems), but the LOWER() function on strings can be used to perform case-insensitive matching. To show how, write a query that finds departments whose names contain the string "sci" as a substring, regardless of the case.
    ```
    SELECT *
    FROM department
    WHERE lower(dept_name) LIKE '%sci%';
    ```


##### 3.7 Consider the SQL query

```sql
select p.a1
from p, r1, r2
where p.a1 = r1.a1 or p.a1 = r2.a1
```
    Under what conditions does the preceding query select values of p.a1 that are either in r1 or in r2? Examine carefully the cases where either r1 or r2 may be empty.

##### 3.8 Consider the bank database of Figure 3.18, where the primary keys are underlined. Construct the following SQL queries for this relational database.
```
branch(branch_name, branch_city, assets)
customer(ID, customer_name, customer_street, customer_city)
loan(loan_number, branch_name, amount)
borrower(ID, loan_number)
account(account_number, branch_name, balance)
depositor(ID, account_number)
```
Figure 3.18 Banking database.

    a. Find the ID of each customer of the bank who has an account but not a loan.

    b. Find the ID of each customer who lives on the same street and in the same city as customer '12345'.

    c. Find the name of each branch that has at least one customer who has an account in the bank and who lives in "Harrison".

##### 3.9 Consider the relational database of Figure 3.19, where the primary keys are underlined. Give an expression in SQL for each of the following queries.

    a. Find the ID, name, and city of residence of each employee who works for "First Bank Corporation".

    b. Find the ID, name, and city of residence of each employee who works for "First Bank Corporation" and earns more than $10000.

    c. Find the ID of each employee who does not work for "First Bank Corporation".

    d. Find the ID of each employee who earns more than every employee of "Small Bank Corporation".

    e. Assume that companies may be located in several cities. Find the name of each company that is located in every city in which "Small Bank Corporation" is located.

    f. Find the name of the company that has the most employees (or companies, in the case where there is a tie for the most).

    g. Find the name of each company whose employees earn a higher salary, on average, than the average salary at "First Bank Corporation".

##### 3.10 Consider the relational database of Figure 3.19. Give an expression in SQL for each of the following:

    a. Modify the database so that the employee whose ID is '12345' now lives in "Newtown".

    b. Give each manager of "First Bank Corporation" a 10 percent raise unless the salary becomes greater than $100000; in such cases, give only a 3 percent raise.


#### 4.2 Write the following queries in SQL:

    a. Display a list of all instructors, showing each instructor's ID and the number of sections taught. Make sure to show the number of sections as 0 for instructors who have not taught any section. Your query should use an outer join, and should not use subqueries.

    b. Write the same query as in part a, but using a scalar subquery and not using outer join.

    c. Display the list of all course sections offered in Spring 2018, along with the ID and name of each instructor teaching the section. If a section has more than one instructor, that section should appear as many times in the result as it has instructors. If a section does not have any instructor, it should still appear in the result with the instructor name set to `"—"`.

---

#### 4.3 Outer join expressions can be computed in SQL without using the SQL outer join operation. To illustrate this fact, show how to rewrite each of the following SQL queries without using the outer join expression.

a. 
```sql
SELECT * FROM student NATURAL LEFT OUTER JOIN takes;
```

b.
```
SELECT * FROM student NATURAL FULL OUTER JOIN takes;
```

#### 4.4 Suppose we have three relations r(A, B), s(B, C), and t(B, D), with all attributes declared as not null.

a. Give instances of relations r, s, and t such that in the result of
```
(r NATURAL LEFT OUTER JOIN s) NATURAL LEFT OUTER JOIN t

attribute C has a null value but attribute D has a non-null value.
```
b. Are there instances of r, s, and t such that the result of
```
r NATURAL LEFT OUTER JOIN (s NATURAL LEFT OUTER JOIN t)
```
has a null value for C but a non-null value for D? Explain why or why not.

#### 4.5 Testing SQL queries: To test if a query specified in English has been correctly written in SQL, the SQL query is typically executed on multiple test databases, and a human checks if the SQL query result on each test database matches the intention of the specification in English.

    a. In Section 4.1.1 we saw an example of an erroneous SQL query which was intended to find which courses had been taught by each instructor; the query computed the natural join of instructor, teaches, and course, and as a result it unintentionally equated the dept_name attribute of instructor and coequatedurse. Give an example of a dataset that would help catch this particular error.

    b. When creating test databases, it is important to create tuples in referenced relations that do not have any matching tuple in the referencing relation for each foreign key. Explain why, using an example query on the university database.

    c. When creating test databases, it is important to create tuples with null values for foreign-key attributes, provided the attribute is nullable (SQL allows foreign-key attributes to take on null values, as long as they are not part of the primary key and have not been declared as not null). Explain why, using an example query on the university database.

#### 4.6 Show how to define the view student_grades(ID, GPA) giving the grade-point average of each student, based on the query in Exercise 3.2; recall that we used a relation grade_points(grade, points) to get the numeric points associated with a letter grade. Make sure your view definition correctly handles the case of null values for the grade attribute of the takes relation.

```
CREATE VIEW student_grades(ID, GPA) AS
SELECT ID, credit_points / (CASE WHEN credit_sum = 0 THEN NULL ELSE credit_sum END)
FROM (
  (SELECT ID, SUM(CASE WHEN grade IS NULL THEN 0 ELSE credits END) AS credit_sum,
          SUM(CASE WHEN grade IS NULL THEN 0 ELSE credits * points END) AS credit_points
   FROM (takes NATURAL JOIN course) NATURAL LEFT OUTER JOIN grade_points
   GROUP BY ID)
UNION
SELECT ID, NULL, NULL
FROM student
WHERE ID NOT IN (SELECT ID FROM takes));
```

This query ensures that a student who has not taken any course with non-null credits, and has credit_sum = 0, gets a GPA of null. This avoids division by zero, which would otherwise have resulted.


---

(a) (10pts) Find the ID and name of each student who has taken at least one Comp. Sci. course; make sure
there are no duplicate names in the result.

(b) (10pts) Find the ID and name of each student who has not taken any course offered before 2017.

(c) (10pts) For each department, find the maximum salary of instructors in that department. You may
assume that every department has at least one instructor.

(d) (10pts) Find the lowest, across all departments, of the per-department maximum salary computed by
the preceding query

##### L1 
    - Find the names of all instructors who have
    taught some course and the course_id

    - Find the names of all instructors in the Art
    department who have taught some course and
    the course_id


- Find the names of all instructors who have a higher salary than some instructor in 'Comp. Sci'. **USING rename OPERATION**
```
SELECT DISTINCT name
FROM instructor as i
WHERE i.salary >ANY(
	SELECT salary
	FROM instructor as s
	WHERE s.dept_name ='Comp. Sci.');
```

- Find the names of all instructors whose name includes the substring “dar”. **String Operation** => '% \ ^ $ ||'

- Find the names of all instructors with salary between $90,000 and
$100,000 (that is,>=$90,000 and<=$100,000)

`Tuple comparison`
• select name, course_id
from instructor, teaches
`where (instructor.ID, dept_name) = (teaches.ID, 'Biology')`

** Set Operations** relational algebra로도 풀어보기 !
- Find courses that ran in Fall 2017 or in Spring 2018

- Find courses that ran in Fall 2017 and in Spring 2018
  
- Find courses that ran in Fall 2017 but not in Spring 2018

#### NULL과 UNKNOWN의 차이 & 산술연산 결과 비교 !

1. NULL과 산술 연산의 결과는 항상 NULL
   
![image](https://github.com/user-attachments/assets/dd04c501-c3cd-4f7b-a537-f18e76131866)

##### 집계함수

- Find the total number of instructors who teach a course in the Spring 2018 semester

- Find the average salary of instructors in each department

##### set MEMBERSHIP <in ,not in>


#### set comparision (some,all ,exists , not exists , unique )
- Find all courses taught in both the Fall 2017 semester and in the Spring 2018 semester

- Find all students who have taken all courses offered in the Biology department.

- Find all courses that were offered at most once in 2017



#### With 

- Find the average instructors’ salaries of those departments where the average
salary is greater than $42,000.
