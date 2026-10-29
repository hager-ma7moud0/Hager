import random
from dataclasses import dataclass


@dataclass
class Task:
    name: str
    priority: int
    arrival: int

    def key(self):
        # الأعلى أولوية الأول، ولو الأولوية متساوية اللي وصل أبكر الأول
        return (self.priority, -self.arrival)


class MaxHeap:
    """Max-heap على array (0-based): left = 2i+1, right = 2i+2, parent = (i-1)//2"""

    def __init__(self):
        self.a = []

    def __len__(self):
        return len(self.a)

    @staticmethod
    def _parent(i):
        return (i - 1) // 2

    @staticmethod
    def _left(i):
        return 2 * i + 1

    @staticmethod
    def _right(i):
        return 2 * i + 2

    def _heapify(self, i):
        """MAX-HEAPIFY (iterative): ينزّل القيمة الصغيرة لمكانها. O(log n)"""
        n = len(self.a)
        while True:
            l, r = self._left(i), self._right(i)
            largest = i
            if l < n and self.a[l].key() > self.a[largest].key():
                largest = l
            if r < n and self.a[r].key() > self.a[largest].key():
                largest = r
            if largest == i:
                return
            self.a[i], self.a[largest] = self.a[largest], self.a[i]
            i = largest

    def _sift_up(self, i):
        """يطلّع العنصر لفوق طول ما هو أكبر من أبوه. O(log n)"""
        while i > 0 and self.a[i].key() > self.a[self._parent(i)].key():
            p = self._parent(i)
            self.a[i], self.a[p] = self.a[p], self.a[i]
            i = p

    def insert(self, task):
        self.a.append(task)
        self._sift_up(len(self.a) - 1)

    def maximum(self):
        return self.a[0]

    def extract_max(self):
        if not self.a:
            raise IndexError("heap is empty")
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self._heapify(0)
        return top

    def increase_key(self, i, new_priority):
        if new_priority < self.a[i].priority:
            raise ValueError("new priority is lower than current")
        self.a[i].priority = new_priority
        self._sift_up(i)


if __name__ == "__main__":
    # 1) مثال المحاضرة: A(3), B(9), C(5), D(7) -> B, D, C, A
    h = MaxHeap()
    for t, (name, p) in enumerate([("A", 3), ("B", 9), ("C", 5), ("D", 7)]):
        h.insert(Task(name, p, arrival=t))
    order = [h.extract_max().name for _ in range(len(h))]
    print("Lecture example:", order)
    assert order == ["B", "D", "C", "A"]

    # 2) 20 task عشوائي، نقارن بالترتيب الصح من sorted()
    random.seed(1)
    tasks = [Task(f"T{i}", random.randint(1, 10), arrival=i) for i in range(20)]
    h = MaxHeap()
    for t in tasks:
        h.insert(t)
    got = [h.extract_max().name for _ in range(len(h))]
    expected = [t.name for t in sorted(tasks, key=lambda t: t.key(), reverse=True)]
    print("Run order:", got)
    assert got == expected
    print("OK: heap order matches sorted()")
