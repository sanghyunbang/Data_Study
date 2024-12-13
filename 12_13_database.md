# SQL Server 데이터베이스 전환과 구조 이해

SQL Server에서 데이터베이스 전환과 관련된 개념, 구조, 그리고 Azure SQL Database 환경에서의 제약 사항을 이해하기 쉽게 설명합니다.

---

## 1. 데이터베이스 전환의 의미와 목적

SQL Server는 하나의 서버에서 여러 데이터베이스를 관리할 수 있습니다. 따라서 작업하려는 데이터베이스를 명시적으로 지정해야 합니다. 이를 데이터베이스 전환이라고 합니다.

### 비유로 이해하기
- 데이터베이스를 **책장**이라고 생각해 보세요.
  - 하나의 데이터베이스는 책장의 **한 칸**입니다.
  - `USE master`는 "이제부터 나는 **master라는 칸에 있는 책**만 읽고 작업할 거야."라고 선언하는 것과 같습니다.

### 데이터베이스 전환이 중요한 이유
1. 서버에는 여러 데이터베이스가 있을 수 있습니다.
2. 데이터를 조회하거나 수정하려면, 작업할 데이터베이스를 명시적으로 지정해야 합니다.

### 제한 사항
- **Azure SQL Database**와 같은 클라우드 환경에서는 `USE` 명령어로 데이터베이스를 전환할 수 없습니다.
- 대신, **새로운 연결을 생성하거나 명령어에서 데이터베이스를 명시적으로 지정**해야 합니다.

---

## 2. `[].[]` 구조 이해하기

SQL Server에서는 데이터베이스 객체(테이블, 뷰 등)를 참조할 때 **4단계 식별 체계**를 사용합니다.

### 4단계 식별 체계
```sql
[ServerName].[DatabaseName].[SchemaName].[TableName]
```
- **ServerName**: 데이터베이스가 속한 서버 이름 (보통 생략 가능)
- **DatabaseName**: 작업하려는 데이터베이스 이름
- **SchemaName**: 데이터베이스 안에서 테이블이나 뷰를 그룹화하는 이름
- **TableName**: 실제 테이블 이름

### 두 개만 명시된 경우
예를 들어, `[SalesLT].[Address]`라면:
- **SalesLT**는 **스키마 이름**입니다.
- **Address**는 **테이블 이름**입니다.

#### 왜 데이터베이스 이름이 생략되었을까?
현재 연결된 데이터베이스가 `dp300`이기 때문에 **`SalesLT.Address`**는 기본적으로 `dp300` 데이터베이스 내부의 SalesLT 스키마에 있는 Address 테이블을 가리킵니다.

---

## 3. Object Explorer 아이콘 의미

SQL Server Management Studio(SSMS)의 Object Explorer에서 볼 수 있는 다양한 아이콘은 데이터베이스 구조를 시각적으로 나타냅니다.

### 아이콘의 의미
1. **원통 모양 (데이터베이스)**  
   - 데이터베이스를 나타냅니다.  
   - 예: `dp300`은 현재 연결된 데이터베이스입니다.

2. **파일 모양 (Tables 폴더)**  
   - 데이터베이스 안의 테이블들을 그룹화한 디렉토리를 나타냅니다.

3. **표 모양 (SalesLT.Address 등)**  
   - 개별 테이블 객체를 나타냅니다.
   - 테이블은 데이터를 **행(row)**과 **열(column)**로 저장하는 구조화된 데이터 저장 공간입니다.

---

## 4. SQL 예제

### 데이터 조회하기
`SalesLT.Address` 테이블에서 모든 데이터를 조회하려면:
```sql
SELECT * 
FROM [SalesLT].[Address];
```
- `SalesLT`는 **스키마 이름**
- `Address`는 **테이블 이름**

### 전체 데이터베이스 구조 보기
현재 연결된 데이터베이스 안에 있는 모든 테이블을 확인하려면:
```sql
SELECT * 
FROM INFORMATION_SCHEMA.TABLES;
```

---

## 5. 주요 개념 정리

### 데이터베이스 전환
- `USE` 명령어는 데이터베이스를 변경하는 전통적인 방법입니다.
- Azure SQL Database 환경에서는 `USE` 명령어가 지원되지 않으며, 대신 데이터베이스 이름과 스키마를 명시적으로 지정해야 합니다.

### `[].[]` 구조
- `[스키마 이름].[테이블 이름]` 형식으로 데이터베이스 객체를 참조합니다.
- 데이터베이스 이름이 생략된 경우, 현재 연결된 데이터베이스를 기본으로 사용합니다.

### Object Explorer 아이콘
- **원통**: 데이터베이스
- **파일 모양**: 테이블 그룹
- **표 모양**: 개별 테이블

---

## 6. 추가 학습 리소스
- [SQL Server 공식 문서](https://learn.microsoft.com/en-us/sql/)
- [Azure SQL Database 가이드](https://learn.microsoft.com/en-us/azure/azure-sql/)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# SQL JOINs: Left and Right Tables Explained

## What is a SQL JOIN?
SQL JOIN combines rows from two or more tables based on a related column. It is essential for querying data stored across multiple tables in a relational database.

## Understanding Left and Right Tables in JOINs

### 1. Left and Right Table Definition
- **Left Table (LEFT):** The table mentioned **after `FROM`** in the query.
- **Right Table (RIGHT):** The table mentioned **after `JOIN`** in the query.

### 2. SELECT and Left/Right Relationship
- **`SELECT` Clause:** Specifies the columns to be included in the result set but does not determine which table is LEFT or RIGHT.
- **`FROM` Clause:** Determines the LEFT table.
- **`JOIN` Clause:** Determines the RIGHT table.

### Example Query
```sql
SELECT Orders.OrderID, Customers.Name, Customers.City
FROM Orders
INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID;
```
- **LEFT Table:** Orders
- **RIGHT Table:** Customers
- **SELECT:** Specifies columns from both tables to be included in the output.

---

## Types of SQL JOINs

### 1. INNER JOIN
- **Definition:** Returns rows with matching values in both LEFT and RIGHT tables.
- **SQL Example:**
  ```sql
  SELECT Student.Name, Grade.Grade
  FROM Student
  INNER JOIN Grade ON Student.StudentID = Grade.StudentID;
  ```
- **Result:** Only students with grades will appear in the result.

### 2. LEFT JOIN (LEFT OUTER JOIN)
- **Definition:** Returns all rows from the LEFT table and matching rows from the RIGHT table. Unmatched rows in the RIGHT table appear as `NULL`.
- **SQL Example:**
  ```sql
  SELECT Student.Name, Grade.Grade
  FROM Student
  LEFT JOIN Grade ON Student.StudentID = Grade.StudentID;
  ```
- **Result:** All students appear, even if they don't have a grade (their grade will show as `NULL`).

### 3. RIGHT JOIN (RIGHT OUTER JOIN)
- **Definition:** Returns all rows from the RIGHT table and matching rows from the LEFT table. Unmatched rows in the LEFT table appear as `NULL`.
- **SQL Example:**
  ```sql
  SELECT Student.Name, Grade.Grade
  FROM Student
  RIGHT JOIN Grade ON Student.StudentID = Grade.StudentID;
  ```
- **Result:** All grades appear, even if no student is linked to them (student name will show as `NULL`).

### 4. FULL JOIN (FULL OUTER JOIN)
- **Definition:** Returns all rows from both LEFT and RIGHT tables. Unmatched rows in either table appear as `NULL`.
- **SQL Example:**
  ```sql
  SELECT Student.Name, Grade.Grade
  FROM Student
  FULL OUTER JOIN Grade ON Student.StudentID = Grade.StudentID;
  ```
- **Result:** Includes all students and all grades, with unmatched values appearing as `NULL`.

### 5. CROSS JOIN
- **Definition:** Returns the Cartesian product of both tables (every row from the LEFT table is combined with every row from the RIGHT table).
- **SQL Example:**
  ```sql
  SELECT Student.Name, Grade.Grade
  FROM Student
  CROSS JOIN Grade;
  ```
- **Result:** Every possible combination of students and grades.

---

## How SELECT Works in JOINs
- The `SELECT` clause specifies which columns to include in the output, but it does not influence which table is LEFT or RIGHT.
- Example:
  ```sql
  SELECT Orders.OrderID, Customers.Name
  FROM Orders
  LEFT JOIN Customers ON Orders.CustomerID = Customers.CustomerID;
  ```
  - `LEFT JOIN` ensures all rows from `Orders` appear.
  - `SELECT` decides which columns to display: `Orders.OrderID` and `Customers.Name`.

---

## Key Takeaways
1. **LEFT Table:** Always the table after `FROM`.
2. **RIGHT Table:** Always the table after `JOIN`.
3. **SELECT Clause:** Specifies the columns in the output, independent of LEFT/RIGHT roles.
4. **JOIN Types:** Determine which rows are included in the final result.

---

## Example Summary
### Query:
```sql
SELECT Orders.OrderID, Customers.Name
FROM Orders
LEFT JOIN Customers ON Orders.CustomerID = Customers.CustomerID;
```
- **LEFT Table:** Orders
- **RIGHT Table:** Customers
- **Result:** All orders are shown. If an order has no matching customer, the `Name` column will be `NULL`.

---

For more examples, refer to your SQL database and practice these JOINs with real data!

--------------------------------------------------------------------------------------------------------------------------------------------------------------

# SQL Query Performance Optimization

Optimizing query performance often starts with understanding and determining the appropriate type of execution plan. This document provides a detailed explanation of execution plans, including their components, analysis, and optimization techniques.

---

## 1. What is an Execution Plan?
An **execution plan** is a step-by-step guide that the database uses to execute a SQL query efficiently. It includes information on how tables are accessed, which indexes are used, and the join algorithms selected.

Think of it as the **travel itinerary** for your query’s journey to retrieve the desired results.

- **Goal**: Minimize execution time and resource usage (e.g., CPU, memory, disk I/O).

---

## 2. Understanding with an Analogy
### Analogy: Planning a Trip
Imagine you want to travel to a destination:
- **Direct flight**: The fastest route but may cost more.
- **Combination of bus and train**: Cheaper but takes longer.
- **Walking**: Free but impractical for long distances.

Similarly, a database optimizer evaluates all possible ways to execute a query and chooses the most efficient plan.

---

## 3. Key Components of an Execution Plan
Execution plans can be viewed using tools or commands like `EXPLAIN` in MySQL or PostgreSQL. The plan typically includes the following components:

### Example Command:
```sql
EXPLAIN SELECT * FROM Orders WHERE customer_id = 12345;
```

### Example Output:
```
| id | select_type | table  | type   | possible_keys | key         | key_len | ref  | rows  | Extra             |
|----|-------------|--------|--------|---------------|-------------|---------|------|-------|-------------------|
|  1 | SIMPLE      | Orders | ref    | customer_idx  | customer_id | 4       | const|    10 | Using where       |
```

### Key Terms:
1. **id**: Identifies the query step.
2. **select_type**: Specifies the type of query (e.g., `SIMPLE`, `SUBQUERY`).
3. **table**: Indicates the table being accessed.
4. **type**: Access method used:
   - `ALL`: Full table scan (inefficient for large tables).
   - `index`: Uses an index scan.
   - `ref`: Searches for specific key references.
5. **possible_keys**: Lists indexes that can be used.
6. **key**: The index actually used.
7. **rows**: Number of rows estimated to be scanned.
8. **Extra**: Additional information (e.g., `Using where`, `Using filesort`).

---

## 4. Types of Access Methods

### 1. Full Table Scan (`ALL`)
- **What it does**: Scans every row in the table.
- **When it occurs**: No index exists or the query cannot utilize existing indexes.
- **Optimization**:
  - Add appropriate indexes.
  - Rewrite queries to limit the search scope.

### 2. Index Scan
- **What it does**: Scans an index to find matching rows.
- **When it occurs**: Index is used to narrow down the search.
- **Optimization**:
  - Ensure relevant columns are indexed.

### 3. Join Processing
- **Nested Loop Join**: Iterates through one table for each matching row in another table.
- **Hash Join**: Builds a hash table for one input and probes it with the other.
- **Merge Join**: Requires sorted input and merges the rows efficiently.

---

## 5. How to Analyze and Optimize Execution Plans

### Step 1: View the Execution Plan
Use the `EXPLAIN` or `EXPLAIN ANALYZE` command to retrieve the execution plan for a query.
```sql
EXPLAIN SELECT * FROM Products WHERE price > 1000;
```

### Step 2: Analyze Problem Areas
Focus on columns such as `type` and `Extra` for inefficiencies:
- **`type = ALL`**: Indicates a full table scan.
- **`Extra = Using filesort`**: Indicates sorting that could be avoided with proper indexing.

### Step 3: Apply Optimization Techniques
1. **Add Indexes**: 
   ```sql
   CREATE INDEX idx_price ON Products(price);
   ```
2. **Rewrite Queries**:
   Avoid `SELECT *` and retrieve only necessary columns.
   ```sql
   SELECT name, price FROM Products WHERE price > 1000;
   ```
3. **Change Joins**:
   Optimize join conditions and ensure indexed columns are used for filtering.

---

## 6. Practical Examples

### Example 1: Optimizing a Simple Query
#### Query:
```sql
SELECT * FROM Orders WHERE customer_id = 12345;
```

#### Execution Plan:
```
| id | select_type | table  | type | possible_keys | key  | rows  | Extra |
|----|-------------|--------|------|---------------|------|-------|-------|
|  1 | SIMPLE      | Orders | ALL  | NULL          | NULL | 10000 | NULL  |
```

#### Problem:
- Full table scan (`type = ALL`).

#### Solution:
1. Add an index on `customer_id`:
   ```sql
   CREATE INDEX idx_customer_id ON Orders(customer_id);
   ```
2. Check the plan again:
   ```sql
   EXPLAIN SELECT * FROM Orders WHERE customer_id = 12345;
   ```
   
   Updated Plan:
   ```
   | id | select_type | table  | type | possible_keys | key         | rows | Extra |
   |----|-------------|--------|------|---------------|-------------|------|-------|
   |  1 | SIMPLE      | Orders | ref  | customer_idx  | customer_id |   10 | NULL  |
   ```

---

## 7. Tools and Resources

### Commands and Tools:
1. **`EXPLAIN`**: Displays the query execution plan.
2. **`EXPLAIN ANALYZE`**: Executes the query and provides runtime statistics (PostgreSQL).
3. **Query Profilers**: Tools like MySQL Workbench or pgAdmin provide graphical insights into execution plans.

### Further Reading:
- [MySQL EXPLAIN Documentation](https://dev.mysql.com/doc/refman/8.0/en/explain.html)
- [SQL Performance Explained](https://use-the-index-luke.com/)

---

## 8. Practice Exercises
1. Optimize the following query:
   ```sql
   SELECT * FROM Products WHERE category = 'Electronics';
   ```
2. Use `EXPLAIN` to identify inefficiencies in the query below:
   ```sql
   SELECT * FROM Orders o JOIN Customers c ON o.customer_id = c.id;
   ```
3. Rewrite the query to reduce execution time by adding indexes and filtering unnecessary data.

---



