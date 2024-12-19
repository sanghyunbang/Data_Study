# 🚀 SQL Execution Plan 최적화 학습 자료

## 🌟 학습 목표
- SQL 쿼리 최적화를 통해 실행 계획(Execution Plan)을 이해하고 성능을 개선합니다.
- **Index Scan**과 **Index Seek**의 차이점과 사용 방법을 이해합니다.
- **Sargable**한 쿼리 작성 방법을 학습합니다.

---

## 📂 실습 데이터베이스 설정 및 쿼리 예제

1️⃣ 데이터베이스 생성 및 초기화

-- 데이터베이스 생성
CREATE DATABASE LearningDB;
USE LearningDB;

-- Users 테이블 생성
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    UserName NVARCHAR(50),
    Age INT,
    JoinDate DATE,
    City NVARCHAR(50)
);

-- 샘플 데이터 삽입
INSERT INTO Users (UserName, Age, JoinDate, City)
VALUES 
('Alice', 25, '2023-01-15', 'Seoul'),
('Bob', 30, '2022-05-20', 'Busan'),
('Charlie', 35, '2023-07-30', 'Incheon'),
('Diana', 40, '2021-11-10', 'Daegu'),
('Eve', 28, '2022-12-01', 'Seoul');

2️⃣ 기본 문제: 인덱스가 없는 경우 (Table Scan 발생)

-- 전체 데이터 조회 (비효율적)
SELECT * FROM Users WHERE Age > 30;

-- 실행 계획 확인 (SQL Server Management Studio에서 실행)
-- 실행 계획 버튼을 클릭하여 실행 계획을 확인
결과: 모든 데이터를 읽는 Table Scan 발생 → 성능 저하.

3️⃣ 해결 방법: 인덱스 생성 및 활용

3.1 Clustered Index 생성

-- Clustered Index 생성
CREATE CLUSTERED INDEX idx_Users_JoinDate ON Users(JoinDate);

3.2 Non-Clustered Index 생성

-- Non-Clustered Index 생성
CREATE NONCLUSTERED INDEX idx_Users_City ON Users(City);

3.3 Non-Clustered Index를 활용한 효율적 쿼리

-- 효율적인 쿼리
SELECT * FROM Users WHERE City = 'Seoul';

3.4 Non-Sargable 쿼리의 예제

-- 비효율적 쿼리 (Non-Sargable)
SELECT * FROM Users WHERE YEAR(JoinDate) = 2023;

3.5 Sargable 개선

-- 효율적인 쿼리 (Sargable)
SELECT * FROM Users 
WHERE JoinDate BETWEEN '2023-01-01' AND '2023-12-31';

실행 계획 확인: SQL Server Management Studio에서 실행 계획을 확인하여 Index Seek 발생 여부를 확인하세요.

🎯 핵심 요약

Table Scan은 성능을 저하시킵니다. → 인덱스를 활용하여 Index Seek으로 개선합니다.
Sargable 쿼리는 인덱스를 효율적으로 사용하여 실행 계획을 최적화할 수 있습니다.
Clustered Index와 Non-Clustered Index를 적재적소에 활용하는 것이 중요합니다.
