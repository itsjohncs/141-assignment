# stdlib
import subprocess

def score(a, b, smith_binary = "./smith.out", result_queue = None):
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
