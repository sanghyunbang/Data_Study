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

# SQL 쿼리 성능 최적화

SQL 쿼리의 성능을 최적화하려면 먼저 실행 계획의 유형을 이해하고 적절히 선택하는 것이 중요합니다. 이 문서는 실행 계획의 구성 요소, 분석 방법, 최적화 기법을 자세히 설명합니다.

---

## 1. 실행 계획이란?
**실행 계획(Execution Plan)**은 데이터베이스가 SQL 쿼리를 효율적으로 실행하기 위해 사용하는 단계별 전략입니다. 테이블에 접근하는 방식, 사용되는 인덱스, 선택된 조인 알고리즘 등을 포함합니다.

실행 계획은 쿼리 결과를 얻기 위한 **여행 경로**와 같습니다.

- **목표**: 실행 시간을 최소화하고 CPU, 메모리, 디스크 I/O와 같은 자원을 효율적으로 사용하는 것입니다.

---

## 2. 비유로 이해하기
### 여행 계획 비유
어떤 목적지에 도착하려 한다고 가정합시다:
- **직항 비행기**: 가장 빠르지만 비용이 많이 듭니다.
- **버스와 기차를 조합**: 저렴하지만 시간이 오래 걸립니다.
- **도보 이동**: 무료지만 먼 거리에 비효율적입니다.

마찬가지로, 데이터베이스 최적화 도구는 쿼리를 실행하는 다양한 방법을 평가하고 가장 효율적인 계획을 선택합니다.

---

## 3. 실행 계획의 주요 구성 요소
실행 계획은 MySQL이나 PostgreSQL에서 `EXPLAIN` 같은 명령어를 통해 확인할 수 있습니다. 일반적으로 다음과 같은 정보를 포함합니다:

### 예시 명령어:
```sql
EXPLAIN SELECT * FROM Orders WHERE customer_id = 12345;
```

### 예시 출력:
```
| id | select_type | table  | type   | possible_keys | key         | key_len | ref  | rows  | Extra             |
|----|-------------|--------|--------|---------------|-------------|---------|------|-------|-------------------|
|  1 | SIMPLE      | Orders | ref    | customer_idx  | customer_id | 4       | const|    10 | Using where       |
```

### 주요 용어:
1. **id**: 쿼리 단계 식별자.
2. **select_type**: 쿼리 유형을 나타냄 (예: `SIMPLE`, `SUBQUERY`).
3. **table**: 접근 중인 테이블 이름.
4. **type**: 테이블 액세스 방식:
   - `ALL`: 전체 테이블 스캔 (대규모 테이블에서는 비효율적).
   - `index`: 인덱스만 스캔.
   - `ref`: 특정 키 참조 검색.
5. **possible_keys**: 사용할 수 있는 인덱스 목록.
6. **key**: 실제 사용된 인덱스.
7. **rows**: 스캔해야 할 행 수의 추정치.
8. **Extra**: 추가 정보 (예: `Using where`, `Using filesort`).

---

## 4. 테이블 액세스 방식

### 1. 전체 테이블 스캔 (`ALL`)
- **설명**: 테이블의 모든 행을 스캔.
- **발생 상황**: 인덱스가 없거나, 쿼리가 기존 인덱스를 활용하지 못하는 경우.
- **최적화**:
  - 적절한 인덱스를 추가.
  - 쿼리를 재작성하여 검색 범위를 제한.

### 2. 인덱스 스캔
- **설명**: 인덱스를 스캔하여 일치하는 행을 검색.
- **발생 상황**: 인덱스를 활용하여 검색 범위를 줄임.
- **최적화**:
  - 관련 열에 인덱스를 추가.

### 3. 조인 처리
- **중첩 루프 조인(Nested Loop Join)**: 한 테이블의 각 행에 대해 다른 테이블의 일치하는 행을 검색.
- **해시 조인(Hash Join)**: 한 테이블의 데이터를 해시 테이블로 생성하고, 이를 이용해 다른 테이블을 검색.
- **병합 조인(Merge Join)**: 정렬된 데이터를 병합하여 처리.

---

## 5. 실행 계획 분석 및 최적화 방법

### 1단계: 실행 계획 확인
`EXPLAIN` 또는 `EXPLAIN ANALYZE` 명령어를 사용하여 쿼리의 실행 계획을 확인합니다.
```sql
EXPLAIN SELECT * FROM Products WHERE price > 1000;
```

### 2단계: 문제 영역 분석
`type`과 `Extra` 같은 컬럼을 중점적으로 확인:
- **`type = ALL`**: 전체 테이블 스캔.
- **`Extra = Using filesort`**: 정렬을 피하기 위해 추가 최적화 필요.

### 3단계: 최적화 기법 적용
1. **인덱스 추가**:
   ```sql
   CREATE INDEX idx_price ON Products(price);
   ```
2. **쿼리 재작성**:
   `SELECT *` 대신 필요한 열만 검색.
   ```sql
   SELECT name, price FROM Products WHERE price > 1000;
   ```
3. **조인 최적화**:
   조인 조건을 개선하고 인덱스를 활용.

---

## 6. 실전 예제

### 예제 1: 간단한 쿼리 최적화
#### 문제:
```sql
SELECT * FROM Orders WHERE customer_id = 12345;
```

#### 실행 계획:
```
| id | select_type | table  | type | possible_keys | key  | rows  | Extra |
|----|-------------|--------|------|---------------|------|-------|-------|
|  1 | SIMPLE      | Orders | ALL  | NULL          | NULL | 10000 | NULL  |
```

#### 문제점:
- 전체 테이블 스캔 (`type = ALL`).

#### 해결:
1. `customer_id`에 인덱스를 추가:
   ```sql
   CREATE INDEX idx_customer_id ON Orders(customer_id);
   ```
2. 실행 계획 재확인:
   ```sql
   EXPLAIN SELECT * FROM Orders WHERE customer_id = 12345;
   ```
   
   업데이트된 실행 계획:
   ```
   | id | select_type | table  | type | possible_keys | key         | rows | Extra |
   |----|-------------|--------|------|---------------|-------------|------|-------|
   |  1 | SIMPLE      | Orders | ref  | customer_idx  | customer_id |   10 | NULL  |
   ```

---

## 7. 서브쿼리

### 서브쿼리란?
**서브쿼리(Subquery)**는 다른 SQL 쿼리 안에 중첩된 쿼리입니다. 중간 계산이나 필터링을 수행하기 위해 사용됩니다. 서브쿼리는 `SELECT`, `FROM`, `WHERE` 절에 나타날 수 있습니다.

### 서브쿼리 유형:
1. **스칼라 서브쿼리**:
   - 단일 값을 반환.
   - **예시**:
     ```sql
     SELECT name FROM Products WHERE price = (SELECT MAX(price) FROM Products);
     ```
2. **행 서브쿼리**:
   - 단일 행을 반환.
   - **예시**:
     ```sql
     SELECT name FROM Products WHERE (category, price) = (SELECT category, MAX(price) FROM Products GROUP BY category);
     ```
3. **테이블 서브쿼리**:
   - 다중 행 또는 전체 테이블을 반환.
   - **예시**:
     ```sql
     SELECT name FROM Products WHERE category IN (SELECT category FROM Categories WHERE active = 1);
     ```

### 서브쿼리 vs. 조인:
- 서브쿼리는 작성이 간단하지만 대규모 데이터셋에서 성능이 떨어질 수 있음.
- 조인은 별도의 쿼리 실행 없이 더 효율적.

---

## 8. 도구 및 참고 자료

### 명령어 및 도구:
1. **`EXPLAIN`**: 실행 계획 확인.
2. **`EXPLAIN ANALYZE`**: 쿼리를 실행하고 런타임 통계를 제공 (PostgreSQL).
3. **쿼리 프로파일러**: MySQL Workbench, pgAdmin 등 시각적 실행 계획 도구.

### 참고 자료:
- [MySQL EXPLAIN Documentation](https://dev.mysql.com/doc/refman/8.0/en/explain.html)
- [SQL Performance Explained](https://use-the-index-luke.com/)

---

## 9. 연습 문제
1. 다음 쿼리를 최적화하세요:
   ```sql
   SELECT * FROM Products WHERE category = 'Electronics';
   ```
2. 아래 쿼리에서 실행 계획을 확인하고 비효율성을 찾아보세요:
   ```sql
   SELECT * FROM Orders o JOIN Customers c ON o.customer_id = c.id;
   ```
3. 인덱스를 추가하고 불필요한 데이터를 제거하여 쿼리를 최적화하세요.

---



