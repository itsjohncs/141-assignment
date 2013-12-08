# stdlib
import heapq

class PriorityQueue:
    """A simple min-priority-queue that uses the heapq library."""

    def __init__(self, items = None):
        if items is None:
            self._heap = []
        else:
            self._heap = list(items)
            heapq.heapify(self._heap)

    def push(self, item):
        heapq.heappush(self._heap, item)

    def pop(self):
        return heapq.heappop(self._heap)

    def top(self):
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return len(self._heap) != 0
