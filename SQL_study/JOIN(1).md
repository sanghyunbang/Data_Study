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

