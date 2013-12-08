# stdlib
import os

# internal
from . import data
from .. import scorefunc

# external
import pytest

# Figure out what samples we have available when the module is imported so
# we can use it below.
_scores_dir = os.path.join(data.get_directory(), "scorefiles")
_samples = [os.path.join(_scores_dir, i) for i in os.listdir(_scores_dir)
    if i.endswith(".ini")]

@pytest.mark.parametrize("sample", _samples)
def test_sample_files(sample):
    sample_file = open(sample, "r")

    sub_score, gap_score = scorefunc.make_score_functions(sample_file)

    # Perform any assertions
    pyfile_path = sample[:-4] + ".py" # cuts off the .txt and adds .py
    exec open(pyfile_path, "r")

def test_default():
    sub_score, gap_score = scorefunc.make_score_functions(None)

    pyfile_path = os.path.join(
        data.get_directory(), "scorefiles", "default.py")
    exec open(pyfile_path, "r")

