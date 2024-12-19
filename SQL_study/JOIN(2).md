# INNER JOIN의 동작과 JOIN 알고리즘 종류

## 1. INNER JOIN이란?
**INNER JOIN**은 두 테이블에서 공통된 값을 기반으로 행(row)을 결합하는 SQL 연산입니다. 
사용자가 SQL 쿼리에서 INNER JOIN을 작성하면, 데이터베이스 엔진은 **테이블 크기, 정렬 상태, 인덱스 유무**에 따라 적합한 JOIN 알고리즘을 선택해 실행합니다.

## 2. INNER JOIN에서 사용되는 JOIN 알고리즘
INNER JOIN은 내부적으로 다음과 같은 알고리즘으로 실행됩니다:

### 🔄 2.1 Nested Loop Join
- **작은 데이터셋**에 적합한 방식입니다.
- 두 테이블 중 하나의 각 행을 다른 테이블의 모든 행과 비교하여 조건을 만족하는 데이터를 반환합니다.
- **중첩된 반복문(Nested Loop)**처럼 동작하기 때문에 이런 이름이 붙었습니다.

### 🧩 2.2 Merge Join
- **정렬된 테이블**에 적합한 방식입니다.
- 두 테이블이 정렬되어 있으면, 각 테이블의 첫 번째 행부터 조건을 비교하며 효율적으로 매칭합니다.
- 정렬이 필요할 경우 추가적인 정렬 비용이 발생합니다.

### 🔍 2.3 Hash Join
- **정렬되지 않은 데이터**나 **큰 데이터셋**에서 효과적입니다.
- 한 테이블을 **Hash Table**로 변환한 뒤, 다른 테이블과 매칭하여 조건을 만족하는 데이터를 반환합니다.
- 메모리 사용량이 많을 수 있습니다.

---

## 3. Nested Loop Join 상세 설명

### 3.1 개념
- Nested Loop Join은 **두 테이블의 행을 반복적으로 비교**하여 조건을 만족하는 데이터를 반환하는 방식입니다.
- 하나의 테이블(Outer Table)의 각 행마다, 다른 테이블(Inner Table)의 모든 행과 비교합니다.

### 3.2 왜 Nested(중첩)이고 Loop(반복)인가?
- **중첩(Nested)**: Outer Table의 한 행에 대해 Inner Table의 모든 행을 비교하므로 중첩된 구조를 가집니다.
- **반복(Loop)**: 테이블의 모든 데이터를 조건에 따라 반복적으로 비교하므로 반복문이 사용됩니다.

### 3.3 작동 원리
1. Outer Table(외부 테이블)에서 첫 번째 행을 가져옵니다.
2. Inner Table(내부 테이블)의 모든 행과 비교합니다.
3. 조건이 일치하면 해당 행을 결과로 반환합니다.
4. Outer Table의 다음 행으로 이동하며 이 과정을 반복합니다.

### 3.4 구체적인 예시
#### 테이블 구조
1. **Employees 테이블**:
   | EmployeeID | Name     | DepartmentID |
   |------------|----------|--------------|
   | 1          | Alice    | 10           |
   | 2          | Bob      | 20           |
   | 3          | Charlie  | 30           |

2. **Departments 테이블**:
   | DepartmentID | DepartmentName |
   |--------------|----------------|
   | 10           | HR             |
   | 20           | IT             |
   | 30           | Finance        |

#### SQL 쿼리
```sql
SELECT E.EmployeeID, E.Name, D.DepartmentName
FROM Employees E
INNER JOIN Departments D
ON E.DepartmentID = D.DepartmentID;
```

#### 실행 과정
1. Outer Table `Employees`의 첫 번째 행 (`EmployeeID = 1`)을 가져옵니다.
   - Inner Table `Departments`에서 `DepartmentID = 10`인 행을 찾습니다.
   - 조건 일치: `Alice (HR)` -> 결과에 추가.

2. 다음으로 Outer Table의 두 번째 행 (`EmployeeID = 2`)로 이동합니다.
   - Inner Table에서 `DepartmentID = 20`인 행을 찾습니다.
   - 조건 일치: `Bob (IT)` -> 결과에 추가.

3. 마지막으로 Outer Table의 세 번째 행 (`EmployeeID = 3`)을 가져옵니다.
   - Inner Table에서 `DepartmentID = 30`인 행을 찾습니다.
   - 조건 일치: `Charlie (Finance)` -> 결과에 추가.

#### 결과 데이터
| EmployeeID | Name     | DepartmentName |
|------------|----------|----------------|
| 1          | Alice    | HR             |
| 2          | Bob      | IT             |
| 3          | Charlie  | Finance        |

---

### 3.5 장점과 단점
#### ✅ 장점
- **간단하고 직관적**인 방식입니다.
- **작은 데이터셋**이나 적절한 인덱스가 있는 경우 효율적입니다.

#### ⚠️ 단점
- 테이블 크기가 클 경우, 모든 행을 비교하므로 **성능 저하**가 발생할 수 있습니다.
- Inner Table이 클수록 처리 시간이 크게 증가합니다.

---

## 4. Merge Join 상세 설명

### 4.1 개념
- Merge Join은 **정렬된 두 테이블**을 기반으로, 조건을 만족하는 데이터를 빠르게 결합하는 방식입니다.
- 두 테이블이 정렬되어 있는 경우, 각 테이블의 커서를 동시에 이동하며 조건을 비교합니다.

### 4.2 작동 원리
1. 두 테이블을 조인 열 기준으로 정렬합니다. (이미 정렬된 경우 생략)
2. 각 테이블의 첫 번째 행부터 비교합니다.
3. 조건이 일치하면 해당 행을 결과에 추가하고, 두 테이블의 다음 행으로 이동합니다.
4. 조건이 일치하지 않으면 값이 작은 쪽의 다음 행으로 이동합니다.

### 4.3 구체적인 예시
#### 테이블 구조
1. **Orders 테이블**:
   | OrderID | CustomerID |
   |---------|------------|
   | 1       | 101        |
   | 2       | 102        |
   | 3       | 103        |

2. **OrderDetails 테이블**:
   | OrderID | ProductID |
   |---------|-----------|
   | 1       | 1001      |
   | 2       | 1002      |
   | 3       | 1003      |

#### SQL 쿼리
```sql
SELECT O.OrderID, O.CustomerID, OD.ProductID
FROM Orders O
INNER JOIN OrderDetails OD
ON O.OrderID = OD.OrderID
ORDER BY O.OrderID;
```

#### 실행 과정
1. `Orders`와 `OrderDetails` 테이블이 `OrderID` 기준으로 정렬되어 있다고 가정.
2. 첫 번째 행(`OrderID = 1`) 비교 -> 조건 만족 -> 결과에 추가.
3. 두 번째 행(`OrderID = 2`) 비교 -> 조건 만족 -> 결과에 추가.
4. 세 번째 행(`OrderID = 3`) 비교 -> 조건 만족 -> 결과에 추가.

#### 결과 데이터
| OrderID | CustomerID | ProductID |
|---------|------------|-----------|
| 1       | 101        | 1001      |
| 2       | 102        | 1002      |
| 3       | 103        | 1003      |

### 4.4 장점과 단점
#### ✅ 장점
- 정렬된 데이터에서 매우 효율적입니다.
- 대규모 데이터셋에도 적합합니다.

#### ⚠️ 단점
- 데이터가 정렬되지 않은 경우, 정렬 비용이 추가로 발생합니다.

---


## 5. Hash Join 상세 설명

### 5.1 Hash Table의 개념
- **Hash Table**은 데이터를 저장하기 위한 자료구조로, 키와 값을 매핑하는 방식으로 작동합니다.
- 해시 함수는 입력된 키를 고유한 해시 값으로 변환하며, 이를 통해 데이터를 특정 **버킷(Hash Bucket)**에 저장합니다.

### 5.2 Hash Bucket이란?
- **Hash Bucket**은 Hash Table 내부의 저장 슬롯으로, 해시 함수에 의해 계산된 값에 따라 데이터가 저장됩니다.
- 예를 들어, `hash(ProductID) = ProductID % 2`라는 해시 함수가 있다면, ProductID가 1, 3인 데이터는 동일한 Hash Bucket(버킷 1)에 저장될 수 있습니다.
- 하나의 버킷에는 여러 데이터가 저장될 수 있으며, 이는 **해시 충돌(Hash Collision)**을 유발할 수 있습니다.

### 5.3 Hash Match Join이란?
- **Hash Match Join**은 Hash Join의 실행 방식으로, 다음 두 단계를 포함합니다:
  1. **Build 단계**: 작은 테이블을 기반으로 Hash Table을 생성합니다.
  2. **Probe 단계**: 큰 테이블의 각 행을 Hash Table과 비교하여 조건을 만족하는 데이터를 반환합니다.

### 5.4 작동 원리
1. Build 단계: 작은 테이블의 데이터를 해시 함수로 변환하여 Hash Table 생성.
   - 예: `hash(ProductID) = ProductID % 5`를 사용하여 데이터를 5개의 버킷으로 나눕니다.
2. Probe 단계: 큰 테이블의 데이터를 Hash Table에서 검색하여 조건을 만족하는 데이터를 반환.
   - 예: 큰 테이블의 `ProductID`를 동일한 해시 함수로 계산해 Hash Table에서 찾습니다.

### 5.5 구체적인 예시
#### 테이블 구조
1. **Products 테이블**:
   | ProductID | ProductName |
   |-----------|-------------|
   | 1         | Keyboard    |
   | 2         | Mouse       |
   | 3         | Monitor     |

2. **Sales 테이블**:
   | SaleID | ProductID | Quantity |
   |--------|-----------|----------|
   | 1001   | 1         | 10       |
   | 1002   | 2         | 20       |
   | 1003   | 3         | 30       |

#### 해시 함수
- **해시 함수**: `hash(ProductID) = ProductID % 2`
- **Hash Table 생성**:
  - 버킷 0: `ProductID = 2`
  - 버킷 1: `ProductID = 1`, `ProductID = 3`

#### SQL 쿼리
```sql
SELECT P.ProductName, S.Quantity
FROM Products P
INNER JOIN Sales S
ON P.ProductID = S.ProductID;
```

#### 실행 과정
1. Build 단계: `Products` 테이블을 Hash Table로 변환.
   - 키: `ProductID`, 값: `ProductName`.
   - 결과:
     - 버킷 0: `ProductID = 2 (Mouse)`
     - 버킷 1: `ProductID = 1 (Keyboard)`, `ProductID = 3 (Monitor)`
2. Probe 단계: `Sales` 테이블의 각 행의 `ProductID`를 해시 함수로 계산하여 버킷을 검색.
   - `SaleID = 1001`: `ProductID = 1` → 버킷 1에서 찾음 → `Keyboard, 10`
   - `SaleID = 1002`: `ProductID = 2` → 버킷 0에서 찾음 → `Mouse, 20`
   - `SaleID = 1003`: `ProductID = 3` → 버킷 1에서 찾음 → `Monitor, 30`

#### 결과 데이터
| ProductName | Quantity |
|-------------|----------|
| Keyboard    | 10       |
| Mouse       | 20       |
| Monitor     | 30       |

### 5.6 Hash Join의 장점과 단점
#### ✅ 장점
- **정렬이 필요하지 않아** 정렬 비용이 없습니다.
- 대규모 데이터에서도 **빠르게 동작**합니다.

#### ⚠️ 단점
- 해시 충돌이 발생할 가능성이 있습니다.
  - **해시 충돌(Hash Collision)**: 서로 다른 키(예: `ProductID = 1`과 `ProductID = 3`)가 동일한 해시 버킷에 매핑되는 상황.
  - **예시**: 해시 함수 `hash(ProductID) = ProductID % 2`를 사용하면, `ProductID = 1`과 `ProductID = 3`은 모두 버킷 1에 매핑됩니다.
  - 충돌이 발생하면 체이닝이나 선형 탐색 같은 충돌 해결 전략이 필요하며, 이로 인해 조회 속도가 느려질 수 있습니다.

---

### 5.7 해시 충돌 해결 방법
1. **체이닝(Chaining)**:
   - 충돌된 데이터를 링크드 리스트 형태로 저장.
   - 예: 버킷 1 → `[1 → 3]`.

2. **오픈 어드레싱(Open Addressing)**:
   - 충돌이 발생한 경우, 다른 빈 슬롯을 찾아 데이터를 저장.
   - 예: 버킷 1에 `ProductID = 1`, 버킷 2에 `ProductID = 3`.

---
## 6. JOIN 알고리즘의 비유로 이해하기
### 🔄 Nested Loop Join
- **비유**: 두 그룹의 사람들이 서로 일일이 악수를 하는 것.
  - 한 명이 상대 그룹의 모든 사람과 인사.
  - 그룹의 인원이 많아질수록 시간이 많이 걸림.

### 🧩 Merge Join
- **비유**: 정렬된 두 줄에서 차례대로 짝을 맞추는 것.
  - 두 줄이 이미 정렬되어 있으면 한 번만 훑어가며 짝을 찾음.
  - 정렬되지 않았다면, 먼저 줄을 정리하는 데 시간이 걸림.

### 🔍 Hash Join
- **비유**: 사람들이 이름표를 보고 같은 그룹으로 나누는 것.
  - 한 그룹이 이름표를 기준으로 정리된 테이블(Hash Table)을 준비.
  - 다른 그룹이 해당 이름표를 기준으로 빠르게 매칭.
  - 이름표가 엉망이면 시간이 더 걸릴 수 있음.

---

## 7. JOIN 알고리즘 비교
| 알고리즘         | 적합한 상황                        | 장점                              | 단점                        |
|-----------------|----------------------------------|---------------------------------|---------------------------|
| **Nested Loop** | 데이터 크기가 작을 때                | 간단하고, 인덱스 활용 가능             | 데이터 크기가 크면 비효율적           |
| **Merge Join**  | 정렬된 데이터                     | 대규모 데이터에도 효율적               | 정렬 비용 발생 가능                 |
| **Hash Join**   | 정렬되지 않은 데이터, 큰 데이터셋       | 정렬 불필요, 대규모 데이터 처리에 강함      | 메모리 소모 크고, 해시 충돌 가능성 있음 |

---

## 8. Nested Loop Join과의 적합성 판단
- Nested Loop Join은 다음과 같은 상황에서 적합합니다:
  1. 테이블의 크기가 작을 때.
  2. **인덱스가 설정**되어 있어 조건 검색이 빠르게 이루어질 때.
  3. 간단한 조건으로 JOIN이 필요한 경우.

- 데이터가 크거나 정렬된 데이터라면 Merge Join 또는 Hash Join을 사용하는 것이 더 효율적일 수 있습니다.
