# 🚀 Clustered Index와 Non-Clustered Index 상세 학습 자료

## 🌟 학습 목표
- SQL 쿼리 최적화를 위해 Clustered Index와 Non-Clustered Index의 개념과 차이점 이해.
- 실행 계획을 활용하여 인덱스의 성능을 확인하고 최적화 방법 학습.

---

## 📂 인덱스 생성 및 활용 예제

### 📌 데이터베이스 생성 및 초기화
```sql
-- Users 테이블 생성
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT, -- 자동 증가 기본 키
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

### 📌 Clustered Index 생성 및 활용
```sql
-- 1. Clustered Index 생성
CREATE CLUSTERED INDEX idx_Users_JoinDate ON Users(JoinDate);

-- 범위 검색에서 효율적 사용
SELECT * FROM Users WHERE JoinDate BETWEEN '2022-01-01' AND '2022-12-31';
```
- **Clustered Index**는 데이터 자체를 정렬하여 저장.
- **범위 검색**에 매우 유리하며, 테이블당 하나만 생성 가능.

---

### 📌 Non-Clustered Index 생성 및 활용
```sql
-- 2. Non-Clustered Index 생성
CREATE NONCLUSTERED INDEX idx_Users_City ON Users(City);

-- 특정 값 검색에서 효율적 사용
SELECT * FROM Users WHERE City = 'Seoul';
```
- **Non-Clustered Index**는 테이블 데이터와 별도로 저장되는 인덱스 페이지를 생성.
- 여러 개 생성 가능하며, 특정 열 검색에 최적화됨.

---

### 📌 실행 계획 확인
```sql
-- 실행 계획 확인 (SQL Server 기준)
SET SHOWPLAN_TEXT ON; -- 실행 계획 텍스트 출력
SELECT * FROM Users WHERE City = 'Seoul';
SET SHOWPLAN_TEXT OFF;
```
- **Index Seek**: 효율적인 검색을 의미.
- **Index Scan**: 전체 테이블 스캔으로 비효율적.

---

## 📖 Clustered Index와 Non-Clustered Index의 차이

| **특징**                     | **Clustered Index**                           | **Non-Clustered Index**                      |
|------------------------------|-----------------------------------------------|---------------------------------------------|
| **데이터 정렬**              | 테이블 데이터 자체가 인덱스에 따라 정렬됨      | 인덱스 데이터가 별도의 페이지에 저장됨       |
| **테이블당 개수**             | 하나만 생성 가능                              | 여러 개 생성 가능                            |
| **범위 검색**                | 매우 빠름 (데이터가 정렬되어 있음)             | 상대적으로 느림                              |
| **추가 저장 공간**            | 별도 필요 없음 (테이블 자체가 정렬됨)         | 별도의 인덱스 페이지에 추가 공간 필요        |
| **수정/삽입/삭제 성능**       | 느림 (데이터 재정렬 필요)                     | 영향 적음                                   |

---

## 📚 비유를 통한 이해

1. **Clustered Index**는 **책의 목차**와 같음:
   - 책 내용이 목차 순서대로 정렬되어 있음.
   - 특정 범위의 내용을 찾을 때(예: 10페이지~20페이지) 빠르게 접근 가능.

2. **Non-Clustered Index**는 **도서관의 색인 카드**와 같음:
   - 색인 카드는 책의 위치를 알려줄 뿐, 책 내용이 정렬된 것은 아님.
   - 특정 항목(예: 저자 이름)을 기준으로 책을 빠르게 찾을 수 있음.

---

## 📊 실제 예제: 테이블 데이터

| **UserID** | **UserName** | **Age** | **JoinDate**  | **City**  |
|------------|--------------|---------|---------------|-----------|
| 1          | Alice        | 25      | 2023-01-15    | Seoul     |
| 2          | Bob          | 30      | 2022-05-20    | Busan     |
| 3          | Charlie      | 35      | 2023-07-30    | Incheon   |
| 4          | Diana        | 40      | 2021-11-10    | Daegu     |
| 5          | Eve          | 28      | 2022-12-01    | Seoul     |

---

### 📌 Clustered Index 적용된 테이블 (JoinDate 기준 정렬)
| **UserID** | **UserName** | **Age** | **JoinDate**  | **City**  |
|------------|--------------|---------|---------------|-----------|
| 4          | Diana        | 40      | 2021-11-10    | Daegu     |
| 2          | Bob          | 30      | 2022-05-20    | Busan     |
| 5          | Eve          | 28      | 2022-12-01    | Seoul     |
| 1          | Alice        | 25      | 2023-01-15    | Seoul     |
| 3          | Charlie      | 35      | 2023-07-30    | Incheon   |

### 📌 Non-Clustered Index 적용된 테이블 (City 기준 검색)
```text
City = 'Seoul' → UserID = 1, 5
City = 'Busan' → UserID = 2
City = 'Incheon' → UserID = 3
City = 'Daegu' → UserID = 4
```

---

## 🎯 결론
1. **Clustered Index**는 데이터 자체를 정렬하여 범위 검색에서 매우 효율적.
2. **Non-Clustered Index**는 별도의 구조를 만들어 특정 열 검색 성능을 향상.
3. 실행 계획을 통해 인덱스가 제대로 활용되고 있는지 확인.
   - **Index Seek**: 효율적 검색.
   - **Index Scan**: 비효율적 검색.

질문이 있다면 언제든 물어보세요! 😊
