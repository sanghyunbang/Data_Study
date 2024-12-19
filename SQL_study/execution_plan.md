## 🚀 SQL Execution Plan 최적화 학습 자료

## 🌟 학습 목표
- SQL 쿼리 최적화를 통해 실행 계획(Execution Plan)을 이해하고 성능을 개선.
- **Index Scan**과 **Index Seek**의 차이점과 사용 방법 이해.
- **Sargable**한 쿼리 작성 방법 학습.

---

## 📂 실습 데이터베이스 설정 및 쿼리 예제

### 📌 데이터베이스 생성 및 초기화
```sql
-- 데이터베이스 생성 및 사용
CREATE DATABASE LearningDB;
USE LearningDB;

-- Users 테이블 생성
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1), -- 자동 증가 기본 키
    UserName NVARCHAR(50), -- 사용자 이름
    Age INT, -- 나이
    JoinDate DATE, -- 가입 날짜
    City NVARCHAR(50) -- 도시
);

-- 샘플 데이터 삽입
INSERT INTO Users (UserName, Age, JoinDate, City)
VALUES 
('Alice', 25, '2023-01-15', 'Seoul'),
('Bob', 30, '2022-05-20', 'Busan'),
('Charlie', 35, '2023-07-30', 'Incheon'),
('Diana', 40, '2021-11-10', 'Daegu'),
('Eve', 28, '2022-12-01', 'Seoul');
```

---

### 📌 기본 문제: 인덱스가 없는 경우 (Table Scan 발생)
```sql
-- 전체 데이터 조회 (비효율적 쿼리)
SELECT * FROM Users WHERE Age > 30;

-- 실행 계획 확인 방법 (SQL Server Management Studio 기준)
-- 실행 계획 버튼 클릭 후 Table Scan 발생 여부를 확인
```

**문제점**: 테이블 전체를 스캔하기 때문에 데이터가 많아질수록 성능 저하 발생.  
**Table Scan**: 테이블의 모든 데이터를 읽는 방식. 인덱스가 없을 때 주로 발생.

---

### 📌 해결 방법: 인덱스 생성 및 활용
```sql
-- 1. Clustered Index 생성
CREATE CLUSTERED INDEX idx_Users_JoinDate ON Users(JoinDate);

-- 2. Non-Clustered Index 생성
CREATE NONCLUSTERED INDEX idx_Users_City ON Users(City);

-- 3. Non-Clustered Index를 활용한 효율적 쿼리
SELECT * FROM Users WHERE City = 'Seoul';

-- 실행 계획 확인: Index Seek를 사용하는지 확인
```

- **Clustered Index**: 데이터가 물리적으로 정렬된 상태로 저장.
- **Non-Clustered Index**: 데이터와 별도로 인덱스를 저장하며 특정 열 검색에 유리.

---

### 📌 Sargable vs Non-Sargable 쿼리 비교
```sql
-- 1. Non-Sargable 쿼리 (비효율적)
SELECT * FROM Users WHERE YEAR(JoinDate) = 2023;

-- 2. Sargable 쿼리 (효율적)
SELECT * FROM Users 
WHERE JoinDate BETWEEN '2023-01-01' AND '2023-12-31';
```

- **Non-Sargable**: 함수(YEAR)를 사용하여 인덱스를 비활성화 → Index Scan 발생.
- **Sargable**: 조건에 함수나 계산이 없어 인덱스 사용 가능 → Index Seek 발생.

---

### 📌 실행 계획 해석 방법
**SQL Server Management Studio(SSMS)**에서 실행 계획을 활성화:
- `Ctrl + M` 또는 "실행 계획 표시" 버튼 클릭.

**실행 계획의 아이콘 해석**:
- **Table Scan**: 데이터 전체를 스캔 (비효율적).
- **Index Seek**: 특정 조건으로 데이터 검색 (효율적).

---

## 🎯 핵심 요약
1. Table Scan은 성능 저하를 유발 → Index Seek으로 개선.
2. Sargable 쿼리 작성으로 인덱스를 최대한 활용.
3. Clustered Index와 Non-Clustered Index의 차이를 이해하고 적절히 사용.
