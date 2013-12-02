# stdlib
import os

# internal
from . import data
from ..organism import Organism
from .. import database

# stdlib
import os

# external
import pytest

# Figure out what samples we have available when the module is imported so
# we can use  it below.
_databases_dir = os.path.join(data.get_directory(), "databases")
_samples = [os.path.join(_databases_dir, i) for i in os.listdir(_databases_dir)
    if i.endswith(".txt")]

@pytest.mark.parametrize("sample", _samples)
def test_sample_files(sample):
    db = open(sample, "r")

    # The import of the Organism class above allows the py files to use it
    pyfile_path = sample[:-4] + ".py" # cuts off the .txt and adds .py
    expected_result = eval(open(pyfile_path, "r").read())

    assert list(database.load_database(db)) == expected_result
