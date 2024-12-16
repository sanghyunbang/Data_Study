# 🚀 SQL 실행 계획과 JOIN 최적화 배우기

SQL 실행 계획은 **쿼리 성능 최적화**를 위해 꼭 필요한 도구입니다. 이를 통해 병목 구간을 분석하고 효율적인 쿼리 실행 방법을 찾을 수 있습니다.

---

## 🛤️ 실행 계획이란?

SQL Server가 쿼리를 **어떻게 실행할지** 보여주는 **로드맵**입니다.  
실행 계획은 크게 **세 가지**로 나눌 수 있습니다:

1. **Estimated Execution Plan**: 쿼리를 실행하지 않고 **예상 경로**를 보여줍니다.  
2. **Actual Execution Plan**: 쿼리를 실행한 후 **실제 경로**를 보여줍니다.  
3. **Live Query Statistics**: 쿼리 실행 중 **실시간 진행 상황**을 시각적으로 보여줍니다.

---

## 📊 실행 계획의 필요성

실제 업무에서 **느린 쿼리**를 만나면 이런 문제가 발생합니다:

- 🐢 **응답 지연**: 웹사이트가 느려지고 고객 불만이 증가합니다.  
- 🖥️ **서버 부하**: 비효율적인 쿼리가 서버 리소스를 과도하게 사용합니다.  
- ⏳ **비즈니스 지연**: 보고서 생성이나 데이터 분석 시간이 오래 걸립니다.  

### **해결책**
실행 계획을 활용해 **병목**을 찾아내고, 최적화된 실행 방식을 적용합니다.

---

## 🔎 실행 계획과 코드 예제

### 1. Estimated Execution Plan (예상 실행 계획) 📋
쿼리를 실행하지 않고 **예상 경로**만 보여줍니다.  

```sql
SET SHOWPLAN_TEXT ON;
SELECT * 
FROM SalesLT.Address A 
CROSS JOIN SalesLT.Customer B;
```

출력 예시:

```text
|--Hash Match (Inner Join)
   |--Clustered Index Scan (OBJECT:([SalesLT].[Address].[PK_Address]))
   |--Clustered Index Scan (OBJECT:([SalesLT].[Customer].[PK_Customer]))
```

### 2. Actual Execution Plan (실제 실행 계획) ✅
쿼리를 실행한 후 실제 처리 경로와 결과를 보여줍니다.

```sql
SET SHOWPLAN_TEXT OFF;
SELECT A.AddressID, C.CustomerID
FROM SalesLT.Address A
JOIN SalesLT.Customer C
ON A.AddressID = C.CustomerID;
```

### 3. Live Query Statistics (실시간 통계) ⏱️
쿼리 실행 중 각 단계의 진행 상황과 행 수를 실시간으로 표시합니다.  

**활성화 방법**: SSMS에서 "Live Query Statistics"를 활성화합니다.

---

## 🧩 JOIN 최적화 예제

### 1. 문제 상황
두 테이블 `Address`와 `Customer`가 있습니다.  
데이터를 JOIN하는 쿼리가 너무 느립니다! 🐢

### 2. 원인 분석
실행 계획을 통해 **Table Scan**이 발생했음을 확인합니다:  
테이블 전체를 스캔하기 때문에 성능이 저하됩니다.

### 3. 해결 방법
인덱스를 추가해서 성능을 개선합니다.

```sql
CREATE INDEX IX_AddressID ON SalesLT.Address(AddressID);
CREATE INDEX IX_CustomerID ON SalesLT.Customer(CustomerID);
```

**인덱스 추가 후**, 실행 계획을 확인하면 Table Scan이 **Index Seek**로 최적화됩니다. 🚀

---

## 🏗️ 인덱스가 있는 경우에도 느린 이유와 해결책

### 1. 인덱스가 있는데도 느린 이유
`City` 열에 인덱스가 있어도 쿼리가 느린 경우는 아래와 같은 상황일 수 있습니다:

#### a. 복합 인덱스의 비효율성
- 기존 인덱스가 단독 열이 아닌, 다른 열과 함께 구성된 **복합 인덱스(Composite Index)**일 수 있습니다.
- 예를 들어, `State`와 `City`로 구성된 복합 인덱스:
  ```sql
  CREATE INDEX IX_ComplexIndex ON SalesLT.Address(State, City);
  ```
- 이 경우, `State` 조건 없이 `City`만으로 데이터를 검색하면, 인덱스를 제대로 활용하지 못할 수 있습니다.

#### b. 인덱스가 너무 커서 비효율적
- 테이블 행 수가 많고, `City` 값이 다양하지 않을 경우, 인덱스 검색도 느릴 수 있습니다. 
  - 예: "Washington"이라는 값이 너무 자주 반복된다면, SQL Server는 Index Scan을 선택할 가능성이 높습니다.

---

### 2. 해결 방법: 새로운 인덱스 생성
#### a. 단일 열 인덱스 생성
- `City` 열에 대한 단독 인덱스를 생성하면 성능이 크게 개선됩니다:
  ```sql
  CREATE INDEX IX_City ON SalesLT.Address(City);
  ```

#### b. 커버링 인덱스 설계
- 쿼리에서 자주 반환되는 다른 열을 포함하는 **커버링 인덱스**를 생성합니다:
  ```sql
  CREATE INDEX IX_City_Covering ON SalesLT.Address(City) INCLUDE (AddressID, PostalCode);
  ```

#### c. 필터링된 인덱스
- 특정 조건에 맞는 데이터만 검색하도록 **필터링된 인덱스**를 설계합니다:
  ```sql
  CREATE INDEX IX_City_Filtered ON SalesLT.Address(City) WHERE State = 'WA';
  ```

---

## 🎯 실전 적용 요약

| 실행 계획              | 용도                    | 비유                              |
|------------------------|-------------------------|-----------------------------------|
| **Estimated Plan**     | 예상 경로 분석          | 지도 앱에서 경로 예측 🗺️         |
| **Actual Plan**        | 실제 실행 후 경로 확인  | 여행 후 기록 🛤️                  |
| **Live Query Statistics** | 실시간 진행 상황 모니터링 | 네비게이션 실시간 경로 🚗         |

---

## 💡 결론

SQL 실행 계획은 병목 구간을 찾아내고 최적화하는 강력한 도구입니다.

- 쿼리를 더 빠르고 효율적으로 실행합니다.  
- 비즈니스 성능과 서버 안정성을 개선합니다.  

**Tip**: 실습을 통해 **Estimated Plan → Actual Plan → 최적화 단계**를 반복하세요! 🔄
