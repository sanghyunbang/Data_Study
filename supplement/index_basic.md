### Clustered Index와 Nonclustered Index에 대한 자세한 설명

---

### **Clustered Index**

1. **정의**
   - Clustered Index는 테이블의 데이터를 물리적으로 정렬하는 방식입니다. 즉, Index의 Key 값에 따라 테이블의 데이터가 정렬되며, 테이블 자체가 Index에 포함됩니다. 이 때문에 하나의 테이블에는 **하나의 Clustered Index**만 생성할 수 있습니다.

2. **테이블 자체가 Index에 포함된다는 의미**
   - Clustered Index는 단순히 테이블에 대해 추가적인 "정렬된 복사본"을 만드는 것이 아닙니다. 테이블의 데이터 **그 자체**가 Clustered Index 구조의 일부가 됩니다.
   - **하나의 Clustered Index만 생성 가능한 이유**: 데이터가 물리적으로 한 가지 방식으로만 정렬될 수 있기 때문입니다. 예를 들어, 전화번호부를 `성 → 이름`으로 정렬하면서 동시에 `전화번호` 순으로 정렬할 수는 없습니다. 각각의 정렬을 따로 하려면 물리적으로 다른 테이블이 필요하게 됩니다.

3. **특징**
   - **데이터 정렬**: Clustered Index는 데이터를 Key 순서대로 정렬하여 저장합니다. 예를 들어, `LastName`과 `FirstName`을 기준으로 Clustered Index를 생성하면, 테이블의 데이터가 이 순서로 정렬됩니다.
   - **실제 데이터 포함**: Clustered Index의 Leaf Node는 실제 데이터 행을 포함합니다. 즉, Index를 통해 데이터를 검색하면 곧바로 데이터에 접근할 수 있습니다.
   - **높은 검색 성능**: 정렬된 데이터를 기반으로 하기 때문에 특정 Key 값이나 범위를 검색할 때 매우 빠릅니다.
   - **단점**: 데이터가 삽입, 삭제, 업데이트될 때 정렬 상태를 유지해야 하므로, 이 과정에서 추가적인 Overhead가 발생합니다.

4. **실생활 비유**
   - *전화번호부*를 예로 들면, 모든 이름이 성(Last Name) → 이름(First Name) 순으로 정렬되어 있습니다. 
     - 이름이 정렬된 상태이므로, "Smith, John"을 찾을 때 `S` 섹션으로 곧바로 이동할 수 있습니다.
     - 이 정렬은 물리적으로 유지되기 때문에, 다른 방식으로 정렬하려면 전체 전화번호부를 다시 구성해야 합니다.

5. **예시**
   ```sql
   CREATE TABLE PhoneBook (
       LastName NVARCHAR(50),
       FirstName NVARCHAR(50),
       PhoneNumber NVARCHAR(20)
   );

   -- Clustered Index 생성
   CREATE CLUSTERED INDEX IDX_LastName_FirstName
   ON PhoneBook (LastName, FirstName);
   ```
   - 위 예시에서는 `LastName`과 `FirstName`을 기준으로 테이블의 데이터가 정렬됩니다. 
   - 이때, `SELECT * FROM PhoneBook WHERE LastName = 'Smith'` 같은 쿼리는 정렬된 데이터를 빠르게 검색할 수 있습니다.

---

### **Nonclustered Index**

1. **정의**
   - Nonclustered Index는 Clustered Index와 달리, 테이블 데이터와 독립적으로 저장되는 별도의 구조입니다. Index는 Key 값과 데이터의 물리적 위치를 가리키는 **포인터**를 포함합니다.

2. **특징**
   - **정렬 독립성**: Nonclustered Index는 테이블의 정렬 상태와 상관없이 원하는 Key 값에 따라 Index를 생성할 수 있습니다.
   - **포인터 구조**: Nonclustered Index의 Leaf Node는 데이터의 실제 위치를 가리키는 포인터를 저장합니다. 따라서 Index를 사용한 검색 후, 데이터를 가져오기 위해 추가적인 작업(Bookmark Lookup)이 필요할 수 있습니다.
   - **다양한 Index 생성 가능**: 한 테이블에서 여러 개의 Nonclustered Index를 생성할 수 있습니다. 예를 들어, `PhoneNumber`를 기준으로 Nonclustered Index를 생성할 수 있습니다.
   - **Filtered Index 및 INCLUDE 컬럼 지원**: Nonclustered Index는 특정 조건에 따라 데이터를 필터링하거나(INCLUDE 옵션), 추가 컬럼을 포함하여 성능을 최적화할 수 있습니다.

3. **실생활 비유**
   - *도서관의 책 목차*를 떠올려 보세요.
     - 목차는 챕터와 페이지 번호(포인터)로 구성되어 있으며, 책(테이블)과는 독립적으로 저장됩니다.
     - 목차를 통해 특정 챕터를 빠르게 찾아갈 수 있지만, 실제 내용을 확인하려면 해당 페이지로 이동해야 합니다.

4. **예시**
   ```sql
   -- Nonclustered Index 생성
   CREATE NONCLUSTERED INDEX IDX_PhoneNumber
   ON PhoneBook (PhoneNumber);

   -- PhoneNumber로 검색
   SELECT FirstName, LastName
   FROM PhoneBook
   WHERE PhoneNumber = '123-456-7890';
   ```
   - 이 Nonclustered Index는 `PhoneNumber`를 기준으로 정렬된 Index 구조를 생성하며, 쿼리는 이 Index를 사용해 데이터를 검색한 뒤, 해당 포인터를 따라 실제 데이터를 가져옵니다.

---

### **Node와 Leaf Node**

1. **Node의 정의**
   - Node란 Index 구조에서 데이터를 저장하거나 다른 노드를 가리키는 기본 단위를 의미합니다.

2. **Index 구조 설명**
   - Index는 **B-Tree(균형 이진 트리)** 구조로 되어 있습니다.
     - **Root Node**: 트리의 시작점으로, 데이터를 찾기 위한 기준 정보를 포함합니다.
     - **Intermediate Nodes**: Root와 Leaf 사이에 위치하며, 데이터를 탐색하는 경로 역할을 합니다.
     - **Leaf Node**:
       - **Clustered Index**에서는 테이블의 실제 데이터 행이 저장됩니다.
       - **Nonclustered Index**에서는 테이블 데이터의 위치를 나타내는 포인터가 저장됩니다.

3. **실생활 비유**
   - 전화번호부를 트리로 나타낸다고 가정:
     - **Root Node**: "A-M은 왼쪽으로, N-Z는 오른쪽으로 이동" 같은 기준을 가짐.
     - **Intermediate Nodes**: "A-F은 왼쪽, G-M은 오른쪽"처럼 데이터를 세분화.
     - **Leaf Nodes**: 각 노드에 이름과 전화번호 같은 실제 데이터가 저장.

---

### **Bookmark Lookup**

1. **정의**
   - Nonclustered Index를 사용해 데이터를 검색한 뒤, 해당 데이터의 실제 값을 가져오기 위해 테이블이나 Clustered Index를 다시 조회하는 과정을 의미합니다.

2. **작동 방식**
   1. **Nonclustered Index를 통해 키 값 검색**: 예를 들어, `PhoneNumber`로 검색하면 해당 데이터의 위치(RID 또는 Clustered Index 키 값)를 반환합니다.
   2. **RID 또는 Clustered Index 키를 사용해 실제 데이터 조회**: 반환된 값을 기반으로 테이블(Heap) 또는 Clustered Index를 다시 조회하여 필요한 데이터를 가져옵니다.

3. **예시**
   ```sql
   -- PhoneNumber로 검색하는 쿼리
   SELECT LastName, FirstName
   FROM PhoneBook
   WHERE PhoneNumber = '123-456-7890';
   ```
   - Nonclustered Index인 `IDX_PhoneNumber`를 통해 `PhoneNumber` 값이 저장된 위치를 찾습니다.
   - 찾은 위치를 바탕으로 테이블에서 `LastName`과 `FirstName` 값을 가져옵니다.

4. **성능 문제**
   - 여러 행에 대해 Bookmark Lookup이 발생하면, 테이블이나 Clustered Index를 반복적으로 조회해야 하므로 성능이 저하될 수 있습니다.
   - 이를 해결하기 위해 `INCLUDE` 옵션을 사용해 필요한 데이터를 Nonclustered Index에 포함하거나, Covering Index를 생성할 수 있습니다.

---

### **Clustered Index와 Nonclustered Index의 차이점**

| **특징**                  | **Clustered Index**                                      | **Nonclustered Index**                                   |
|---------------------------|---------------------------------------------------------|----------------------------------------------------------|
| **물리적 데이터 정렬**     | 데이터가 Index Key에 따라 물리적으로 정렬됨              | 데이터는 정렬되지 않으며 포인터로 참조                   |
| **Leaf Node**             | 실제 데이터 행 포함                                      | 데이터 위치를 가리키는 포인터 포함                      |
| **생성 가능 개수**         | 테이블 당 하나만 가능                                    | 여러 개 생성 가능                                        |
| **추가 기능**             | Filtering 불가능, 모든 데이터를 포함해야 함              | Filtering 가능, INCLUDE로 추가 컬럼 저장 가능           |
| **성능 특징**             | Key 값 검색이나 범위 검색에 최적화                       | 특정 Key 검색에 빠르지만 추가 데이터가 필요하면 느려질 수 있음 |

---

### **결론**
- Clustered Index는 데이터를 정렬하여 효율적인 검색을 제공하며, Nonclustered Index는 추가적인 정렬 옵션과 유연성을 제공합니다.
- 두 가지를 조합하여 데이터베이스의 성능을 최적화할 수 있습니다.
- Index 설계는 테이블의 특성과 사용 패턴을 고려하여 신중히 결정해야 합니다.
