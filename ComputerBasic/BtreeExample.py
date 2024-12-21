class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # 최소 차수 (t는 자식 수의 최소값)
        self.leaf = leaf  # 리프 노드 여부
        self.keys = []  # 키 리스트
        self.children = []  # 자식 노드 리스트

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)  # 초기에는 루트가 리프
        self.t = t

    def traverse(self):
        def _traverse(node):
            for i in range(len(node.keys)):
                if not node.leaf:
                    _traverse(node.children[i])
                print(node.keys[i], end=" ")
            if not node.leaf:
                _traverse(node.children[-1])

        _traverse(self.root)
        print()

    def search(self, k, node=None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == k:
            return (node, i)

        if node.leaf:
            return None

        return self.search(k, node.children[i])

    def insert(self, k):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, False)
            self.root = s
            s.children.append(root)
            self._split_child(s, 0)
            self._insert_non_full(s, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, parent, i):
        t = self.t
        y = parent.children[i]
        z = BTreeNode(t, y.leaf)
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])

        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

    def delete(self, k):
        self._delete(self.root, k)
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]

    def _delete(self, node, k):
        t = self.t
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == k:
            if node.leaf:
                node.keys.pop(i)
            else:
                if len(node.children[i].keys) >= t:
                    pred = self._get_predecessor(node, i)
                    node.keys[i] = pred
                    self._delete(node.children[i], pred)
                elif len(node.children[i + 1].keys) >= t:
                    succ = self._get_successor(node, i)
                    node.keys[i] = succ
                    self._delete(node.children[i + 1], succ)
                else:
                    self._merge(node, i)
                    self._delete(node.children[i], k)
        elif not node.leaf:
            if len(node.children[i].keys) < t:
                self._fill(node, i)
            self._delete(node.children[i], k)

    def _get_predecessor(self, node, i):
        current = node.children[i]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node, i):
        current = node.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill(self, node, i):
        t = self.t
        if i > 0 and len(node.children[i - 1].keys) >= t:
            self._borrow_from_prev(node, i)
        elif i < len(node.children) - 1 and len(node.children[i + 1].keys) >= t:
            self._borrow_from_next(node, i)
        else:
            if i < len(node.children) - 1:
                self._merge(node, i)
            else:
                self._merge(node, i - 1)

    def _borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i - 1]

        child.keys.insert(0, node.keys[i - 1])
        node.keys[i - 1] = sibling.keys.pop(-1)

        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop(-1))

    def _borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]

        child.keys.append(node.keys[i])
        node.keys[i] = sibling.keys.pop(0)

        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]

        child.keys.append(node.keys.pop(i))
        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        node.children.pop(i + 1)

# Usage Example
t = 3  # Minimum degree
btree = BTree(t)

# Insert elements
for key in [10, 20, 5, 6, 15, 30, 25, 22, 8]:
    btree.insert(key)

print("B-Tree after insertion:")
btree.traverse()

# Delete elements
for key in [6, 15, 20]:
    btree.delete(key)
    print(f"B-Tree after deleting {key}:")
    btree.traverse()
