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


