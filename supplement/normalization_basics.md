# 🗂️ 정규화(Normalization)란?

## 📖 개요
**정규화**는 데이터베이스 설계에서 **데이터 중복을 최소화하고 일관성을 유지**하기 위해 데이터를 구조적으로 나누어 저장하는 과정입니다.

정규화를 통해 **데이터베이스의 효율성**을 높이고, **데이터 무결성**을 유지할 수 있습니다.

---

## 🎯 정규화의 목적
1. **데이터 중복 최소화** 📉
   - 중복 데이터를 제거해 저장 공간을 절약합니다.
2. **데이터 일관성 유지** 🔄
   - 한 곳에서만 데이터를 수정하면 일관성이 유지됩니다.
3. **데이터 무결성 보장** ✅
   - 논리적 오류를 방지하고 신뢰할 수 있는 데이터를 유지합니다.

---

## 📚 정규화 단계
정규화는 단계적으로 진행되며, 각 단계는 특정 문제를 해결합니다. 주요 단계는 다음과 같습니다:

### 1️⃣ **제1정규형 (1NF)**
- **조건**: 모든 컬럼이 원자값(더 이상 나눌 수 없는 값)을 가져야 합니다.
- **문제 해결**: 반복되는 그룹을 제거합니다.

**예시**:
| 주문ID | 고객이름 | 상품목록       |
|--------|----------|----------------|
| 1      | 홍길동   | 노트북, 키보드 |

**1NF 변환 후**:
| 주문ID | 고객이름 | 상품명   |
|--------|----------|----------|
| 1      | 홍길동   | 노트북   |
| 1      | 홍길동   | 키보드   |

### 2️⃣ **제2정규형 (2NF)**
- **조건**: 제1정규형 + **부분 종속성 제거**
   - 기본키에 대해 **모든 비-기본키**가 완전 종속되어야 합니다.
- **문제 해결**: 테이블을 분리해 부분 종속성을 제거합니다.

**예시**:
| 주문ID | 고객이름 | 상품ID | 상품명 |
|--------|----------|--------|--------|

**2NF 변환 후**:
- **주문 테이블**:
| 주문ID | 고객이름 |
|--------|----------|
| 1      | 홍길동   |

- **상품 테이블**:
| 상품ID | 상품명   |
|--------|----------|
| 101    | 노트북   |
| 102    | 키보드   |

- **주문상세 테이블**:
| 주문ID | 상품ID |
|--------|--------|
| 1      | 101    |
| 1      | 102    |

### 3️⃣ **제3정규형 (3NF)**
- **조건**: 제2정규형 + **이행적 종속성 제거**
   - 비-기본키가 다른 비-기본키에 종속되지 않아야 합니다.
- **문제 해결**: 이행 종속성을 제거해 더 세분화된 테이블을 만듭니다.

---

## 🛠️ 정규화와 JOIN의 관계
정규화된 데이터베이스에서는 **데이터를 여러 테이블에 나누어 저장**하기 때문에 **JOIN**을 사용해 다시 결합해야 합니다.

**예시**:
- **Customer 테이블**: 고객 정보
- **Order 테이블**: 주문 정보

JOIN을 통해 다음과 같이 데이터를 결합합니다:
```sql
SELECT Orders.주문ID, Customer.고객이름, Orders.상품명
FROM Orders
INNER JOIN Customer
ON Orders.고객ID = Customer.고객ID;
```

---

## 🎉 결론
**정규화**는 데이터베이스의 효율성과 일관성을 유지하기 위한 필수 과정입니다.

- 데이터 중복 제거 📉
- 데이터 무결성 보장 ✅
- 효율적인 데이터 관리 🔧

하지만 정규화된 데이터베이스는 **JOIN 연산**이 필요하기 때문에 **쿼리의 복잡도**가 증가할 수 있습니다. 상황에 따라 정규화와 비정규화의 **균형**을 맞추는 것이 중요합니다.

---

이제 정규화의 개념과 JOIN의 필요성을 이해했으니 실습을 통해 더 깊이 익혀보세요! 😊
