# 📂 B-Tree와 B+Tree: 데이터베이스 인덱스 구조 이해하기

---

## 🌳 B-트리란?

B-트리는 **대규모 데이터 검색 및 관리**를 위한 트리 구조로, 데이터베이스와 파일 시스템에서 널리 사용됩니다.

### 🔑 B-트리의 핵심 특징
1. **균형 유지**:
   - 모든 리프 노드(leaf)는 같은 깊이를 가짐.
   - 검색, 삽입, 삭제 작업이 항상 일정한 성능 보장.

2. **다중 자식 노드**:
   - 하나의 노드에 여러 개의 키(key)와 자식 노드(child)를 저장.
   - 노드가 꽉 차면 자동으로 **분할(split)**.

3. **데이터 정렬**:
   - 각 노드 내부의 키는 항상 정렬된 상태를 유지.
   - 부모 노드는 자식 노드의 키 범위를 정의.

4. **노드의 최소 및 최대 키 개수**:
   - 각 노드는 최소 \(\lceil m/2 \rceil - 1\)개의 키를 가져야 하며, 최대 \(m-1\)개의 키를 가질 수 있음.

---

## 📐 B-트리의 구조

### 간단한 예시 (\(m = 3\), 한 노드에 최대 3개의 자식 노드):
1. **초기 상태**:
   ```
   [10, 20]
   ```

2. **데이터 추가**: 
   데이터를 정렬하여 추가:
   ```
   [10, 20]
       |
      [5]   [15, 30]
   ```

3. **노드 분할**:
   노드가 꽉 차면 중앙값을 기준으로 분할:
   ```
        [15]
       /    \
    [5, 10] [20, 30]
   ```

---

## 🔍 B-트리의 주요 작업

### 🟢 **검색**
1. 루트 노드에서 키를 비교하며 하위 노드로 이동.
2. 리프 노드에서 데이터를 찾음.

**예시: 20 검색**
- 루트 노드에서 20이 15보다 크므로 오른쪽 자식 노드로 이동.
- 오른쪽 자식 노드 [20, 30]에서 20을 발견.

---

### 🟢 **삽입**
1. 데이터를 정렬된 위치에 삽입.
2. 노드가 꽉 차면 중앙값을 기준으로 분할.

**예시: 25 삽입**
- [20, 30]에 25 추가 → [20, 25, 30].
- 분할 발생:
  ```
        [15, 25]
       /    |    \
    [5, 10] [20] [30]
  ```

---

### 🟢 **삭제**
1. 키를 삭제한 후, 최소 키 개수를 유지하기 위해 병합(merge) 또는 재분배(redistribute) 수행.

**예시: 25 삭제**
- 25 삭제 → 병합 발생.

---

## 🌟 B+트리란?

B+트리는 B-트리의 확장으로 **범위 검색과 순차 접근**을 더욱 효율적으로 수행합니다.

### 🔑 B+트리의 주요 특징
1. **리프 노드에 모든 데이터 저장**:
   - 내부 노드는 인덱스 역할만 수행.
   - 리프 노드에 데이터가 저장되고, 연결 리스트 형태로 연결됨.

2. **범위 검색 최적화**:
   - 리프 노드가 연결되어 있어 빠르게 연속 데이터를 검색 가능.

3. **내부 노드 크기 최적화**:
   - 내부 노드에는 키와 포인터만 저장되므로 더 많은 키를 저장 가능.

---

## 🆚 B-트리와 B+트리 비교

| 특징                  | **B-트리**                             | **B+트리**                               |
|-----------------------|----------------------------------------|------------------------------------------|
| 데이터 저장 위치      | 내부 노드와 리프 노드 모두 저장       | 리프 노드에만 저장                      |
| 범위 검색             | 느림                                   | 빠름 (리프 노드 연결 리스트)           |
| 노드 크기             | 키와 데이터 포함                      | 키와 포인터만 포함 (더 많은 키 저장)   |

---

## 💻 실제 사용 예시: B-트리

### **사용 상황**
- **클러스터형 인덱스**에서 데이터가 정렬된 상태로 저장.

### **쿼리 예제**
#### 1️⃣ 데이터 검색
```sql
SELECT *
FROM Books
WHERE BookID = 50000;
```
- 📂 `Books` 테이블에서 B-트리로 BookID 50000을 검색.

#### 2️⃣ 데이터 삽입
```sql
INSERT INTO Books (BookID, Title, Author)
VALUES (60000, 'SQL Basics', 'John Doe');
```
- 삽입 시 노드가 꽉 차면 분할 발생.

---

## 📊 B+트리의 활용 예시

### **사용 상황**
- 범위 검색이 많은 경우 **B+트리**가 더 효율적.

### **쿼리 예제**
#### 1️⃣ 범위 검색
```sql
SELECT *
FROM Orders
WHERE OrderDate BETWEEN '2024-01-01' AND '2024-01-31';
```
- B+트리는 리프 노드가 연결 리스트로 연결되어 있어 빠르게 검색 가능.

---

## 🛠️ 주의사항
1. **필요 없는 인덱스 남발 금지**:
   - 인덱스가 너무 많으면 삽입/삭제 성능 저하.

2. **정기적인 인덱스 유지 관리**:
   - 인덱스 단편화(fragmentation)를 방지하기 위해 재구성 필요.

3. **쿼리 패턴 분석**:
   - 자주 사용되는 조건에만 인덱스를 생성.

---

## 🎯 결론
- **B-트리**는 효율적인 검색, 삽입, 삭제를 위한 기본 트리 구조.
- **B+트리**는 범위 검색 및 순차 접근이 많은 경우에 최적화된 구조.

👉 데이터베이스 인덱스는 쿼리 성능을 극대화하기 위한 중요한 도구입니다. 사용 목적과 데이터 패턴에 따라 적절히 설계하세요!
