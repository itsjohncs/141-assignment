# stdlib
import heapq

class PriorityQueue:
    """A simple priority-queue that uses the heapq library."""

    class KeyValuePair:
        __slots__ = ("key", "value")

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __cmp__(self, other):
            return int.__cmp__(-self.key, -other.key)

        def __hash__(self):
            return hash(self.key)

        def __repr__(self):
            return "KeyValuePair(%s, %s)" % (self.key, self.value)

    def __init__(self, items = None):
        """
        :param items: A list of two-tuples where the first item in each tuple
            is the key and the second item is the value, or a list of
            KeyValuePair objects.

        """

        if items is None:
            self._heap = []
        else:
            self._heap = [PriorityQueue.KeyValuePair(i, j) for i, j in items]
            heapq.heapify(self._heap)

    def push(self, key, item):
        heapq.heappush(self._heap, PriorityQueue.KeyValuePair(key, item))

    def pop(self):
        return heapq.heappop(self._heap)

    def top(self):
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return len(self._heap) != 0
