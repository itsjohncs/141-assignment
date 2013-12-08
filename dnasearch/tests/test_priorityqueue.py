# internal
from .. import priorityqueue

# stdlib
import random

# Make a shorter name for ourselves
PriorityQueue = priorityqueue.PriorityQueue

SAMPLE_VALUES = [random.randrange(1000) for i in xrange(1000)]

def test_push():
    """Ensures that items pushed into the queue are in the queue."""

    pq = PriorityQueue()
    for i in SAMPLE_VALUES:
        pq.push(i)

    assert set(pq._heap) == set(SAMPLE_VALUES)

def test_construction():
    """Ensures that items given to the constructor are in the queue."""

    pq = PriorityQueue(SAMPLE_VALUES)

    assert set(pq._heap) == set(SAMPLE_VALUES)

def test_length():
    pq = PriorityQueue(SAMPLE_VALUES)

    assert len(pq) == len(SAMPLE_VALUES)

def test_pop():
    """Ensures that items are popped in the right order."""

    pq = PriorityQueue(SAMPLE_VALUES)

    sorted_sample_values = sorted(SAMPLE_VALUES)

    queue_list = []
    while pq:
        queue_list.append(pq.pop())

    assert sorted_sample_values == queue_list

def test_top():
    pq = PriorityQueue(SAMPLE_VALUES)

    while pq:
        top_item = pq.top()
        assert top_item == pq.pop()

