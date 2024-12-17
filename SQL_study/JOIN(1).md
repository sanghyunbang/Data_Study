# 🚀 JOIN의 기초부터 이해하기

## 🧩 1. JOIN이란?
JOIN은 데이터베이스에서 두 개 이상의 테이블을 연결하여 데이터를 가져오는 작업입니다.

- 테이블 간의 **공통 열(Column)**을 기준으로 데이터를 연결합니다.
- [**정규화(Normalization)**](../supplement/normalization_basics.md)를 통해 데이터를 나누어 저장하기 때문에 JOIN이 필요합니다.

### 🎯 예시: 쇼핑몰 데이터 구조
- **Customer 테이블**: 고객의 정보 (고객 ID, 이름, 주소 등)
- **Order 테이블**: 고객의 주문 정보 (주문 ID, 고객 ID, 주문 날짜 등)

**JOIN**을 통해 📊 "어떤 고객이 어떤 주문을 했는지" 알 수 있습니다.

---

## 📚 1.2 JOIN의 기본 종류

### 1️⃣ INNER JOIN
- 두 테이블에서 **공통된 값이 있는 데이터만 반환**합니다.
- **비유**: 두 친구 명단에서 겹치는 친구만 찾는 것 👭.

### 2️⃣ LEFT JOIN
- **왼쪽 테이블의 모든 데이터**와 오른쪽 테이블의 공통된 데이터를 반환합니다. (왼쪽 테이블 우선)
- **비유**: 왼쪽 친구 명단을 기준으로 오른쪽 명단과 겹치는 정보만 추가합니다. 📝

### 3️⃣ RIGHT JOIN
- **오른쪽 테이블의 모든 데이터**와 왼쪽 테이블의 공통된 데이터를 반환합니다. (오른쪽 테이블 우선)

### 4️⃣ FULL OUTER JOIN
- **두 테이블의 모든 데이터**를 반환하며, 공통되지 않는 데이터는 NULL로 표시합니다. 🔄 (합집합)

---

## 🤝 2. INNER JOIN 자세히 알아보기

### 2.1 INNER JOIN이란?
INNER JOIN은 두 테이블의 공통된 값이 있는 데이터만 반환합니다.

**🎭 비유**:
- 축구팀 명단과 농구팀 명단이 있다고 합시다.
  - ⚽ **명단 A (축구팀)**: {영희, 철수, 민수}
  - 🏀 **명단 B (농구팀)**: {철수, 민수, 지영}
  - **INNER JOIN 결과**: 두 팀 모두에 속한 {철수, 민수} ✅

### 🧑‍💻 2.2 SQL에서의 INNER JOIN 예제

#### Customers 테이블
| CustomerID | CustomerName | City      |
|------------|--------------|-----------|
| 1          | John         | New York  |
| 2          | Alice        | London    |
| 3          | Bob          | Paris     |

#### Orders 테이블
| OrderID | CustomerID | OrderDate  |
|---------|------------|------------|
| 101     | 1          | 2024-01-01 |
| 102     | 3          | 2024-01-02 |
| 103     | 4          | 2024-01-03 |

**🛠️ INNER JOIN 쿼리**:
```sql
SELECT Customers.CustomerID, Customers.CustomerName, Orders.OrderID, Orders.OrderDate
FROM Customers
INNER JOIN Orders
ON Customers.CustomerID = Orders.CustomerID;
```

**✅ INNER JOIN 결과**:
| CustomerID | CustomerName | OrderID | OrderDate  |
|------------|--------------|---------|------------|
| 1          | John         | 101     | 2024-01-01 |
| 3          | Bob          | 102     | 2024-01-02 |

**🔍 설명**:
- CustomerID가 **양쪽 테이블에 존재하는 값**만 반환됩니다.
- CustomerID = 4인 데이터는 Customers 테이블에 없으므로 제외 ❌.
- CustomerID = 2인 데이터는 Orders 테이블에 없으므로 제외 ❌.

---

## ⚙️ 3. INNER JOIN의 내부 동작 이해하기

### 🔄 3.1 JOIN의 주요 처리 방식

#### 1️⃣ Nested Loops Join
- **작은 데이터셋**에 적합합니다.
- **비유**: 두 그룹의 사람들이 서로 일일이 악수를 하는 것 🤝.

#### 2️⃣ Merge Join
- **정렬된 테이블**에 적합합니다.
- **비유**: 정렬된 두 줄에서 차례로 짝을 맞추는 것 🧑‍🤝‍🧑.

#### 3️⃣ Hash Match Join
- **큰 데이터셋**에 적합합니다.
- **비유**: 사람들이 이름표를 보고 같은 그룹으로 나누는 것 🔍.

---

## 🛠️ 4. HASH JOIN 자세히 알아보기

### 📊 4.1 HASH JOIN이란?
Hash Join은 하나의 테이블 데이터를 **해시 테이블(Hash Table)**로 변환한 뒤, 다른 테이블과 비교하는 방식입니다.

### 🔧 동작 과정
1. **🔨 Build 단계**: 작은 테이블을 해시 테이블로 변환합니다.
2. **🧩 Probe 단계**: 해시 테이블과 큰 테이블을 비교하여 조건을 충족하는 데이터를 반환합니다.

### 📝 예시 쿼리
```sql
SELECT E.EmployeeID, E.EmployeeName, D.DepartmentName
FROM Employees E
INNER JOIN Departments D
ON E.EmployeeID = D.EmployeeID;
```

---

## 🚦 5. 정리

| JOIN 종류       | 설명                                      |
|-----------------|-------------------------------------------|
| **INNER JOIN**  | 두 테이블에서 공통된 값을 연결합니다.      |
| **HASH JOIN**   | 큰 테이블이나 정렬되지 않은 데이터를 효율적으로 처리합니다. |
| **인덱스**      | 데이터를 빠르게 찾기 위해 사용합니다.      |

---

## ⚡ 6. INNER JOIN 최적화와 인덱스의 역할

### 🛑 INNER JOIN이 느려지는 이유
1. **데이터 양이 너무 많을 때** 📈
   - 테이블 크기가 크면 SQL이 모든 데이터를 비교해야 합니다.
2. **인덱스가 없을 때** 🚫
   - 데이터를 빠르게 찾지 못해 **Table Scan**이 발생합니다.

### 🏎️ 인덱스의 역할
- **비유**: 책의 목차처럼 데이터를 빠르게 찾을 수 있게 합니다 📚.

### ✅ 최적화된 쿼리
```sql
CREATE INDEX IX_EmployeeID ON Employees(EmployeeID);
CREATE INDEX IX_EmployeeID ON Departments(EmployeeID);
```

---

## 🧩 7. HASH JOIN과의 관계
- **조건**: 테이블이 **정렬되지 않은 상태**이거나 데이터 양이 매우 많을 때 선택됩니다.
- **비유**: 큰 테이블의 데이터를 이름표로 그룹 지어 비교하는 방식 🔖.

---

## 🛠️ 8. 실제 상황에서의 적용

### 📝 HEADER와 DETAIL의 개념
- **HEADER**: 상위 정보 (예: 주문 ID, 고객 ID, 주문 날짜) 📝.
- **DETAIL**: 세부 정보 (예: 제품 ID, 수량) 🔎.

**예시**:
```sql
SELECT H.SalesOrderID, H.CustomerID, D.ProductID, D.Quantity
FROM SalesOrderHeader H
INNER JOIN SalesOrderDetail D
ON H.SalesOrderID = D.SalesOrderID;
```

**결과**:
| SalesOrderID | CustomerID | ProductID | Quantity |
|--------------|------------|-----------|----------|
| 1            | 101        | 1001      | 2        |
| 2            | 102        | 1002      | 3        |

---
