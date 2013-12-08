# internal
from .. import priorityqueue

# stdlib
import random

# Make a shorter name for ourselves
PriorityQueue = priorityqueue.PriorityQueue

SAMPLE_VALUES = [
    (random.randrange(1000), random.randrange(1000)) for i in xrange(1000)]
SAMPLE_KEYVALUES = [PriorityQueue.KeyValuePair(i, j) for i, j in SAMPLE_VALUES]

def test_push():
    """Ensures that items pushed into the queue are in the queue."""

    pq = PriorityQueue()
    for i, j in SAMPLE_VALUES:
        pq.push(i, j)

    assert set(pq._heap) == set(SAMPLE_KEYVALUES)

def test_construction():
    """Ensures that items given to the constructor are in the queue."""

    pq = PriorityQueue(SAMPLE_VALUES)

    assert set(pq._heap) == set(SAMPLE_KEYVALUES)

def test_length():
    pq = PriorityQueue(SAMPLE_VALUES)

    assert len(pq) == len(SAMPLE_VALUES)

def test_pop():
    """Ensures that items are popped in the right order."""

    pq = PriorityQueue(SAMPLE_VALUES)

    sorted_sample_values = sorted(SAMPLE_KEYVALUES)

    queue_list = []
    while pq:
        queue_list.append(pq.pop())

    assert sorted_sample_values == queue_list

def test_top():
    pq = PriorityQueue(SAMPLE_VALUES)

    while pq:
        top_item = pq.top()
        assert top_item == pq.pop()

