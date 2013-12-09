# stdlib
import subprocess
import math

# setup logging
import logging
log = logging.getLogger("dnasearch.similarity")

def score(a, b, smith_binary = "./smith.out", result_queue = None,
        chunk_size = 200000):
    """
    :param a: A sequence (the entirity of this sequence may not be used). This
        is the reference string.
    :param b: Another sequence (all of this sequence is used). This is the
        query string.

    """

    max_result = None
    for i in xrange(int(math.ceil(len(a) / float(chunk_size)) + 0.5)):
        left = max(chunk_size * i - len(b), 0)
        right = chunk_size * (i + 1) + len(b)

        cur_result = _score(a[left:right], b, smith_binary, result_queue)
        if max_result is None or max_result[0] < cur_result[0]:
            max_result = cur_result

        log.debug("Added new result with score %s.", max_result[0])

    return max_result

def _score(a, b, smith_binary = "./smith.out", result_queue = None):
    if not a or not b:
        raise ValueError("a and b cannot be empty.")

    smith = subprocess.Popen([smith_binary], stdin = subprocess.PIPE,
        stdout = subprocess.PIPE)
    smith.stdin.write(a + "\n")
    smith.stdin.write(b + "\n")
    smith.stdin.close()

    final_score = int(smith.stdout.readline()) / 100.0
    aligned_a = smith.stdout.readline().strip()
    aligned_b = smith.stdout.readline().strip()

    result = (final_score, aligned_a, aligned_b)
    if result_queue is None:
        return result
    else:
        result_queue.put(result)
