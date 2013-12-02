# stdlib
import pkg_resources
import os

def get_directory():
    """
    Returns a path containing the contents of the data directory. Will extract
    the directory if necessary (if we're in a zip file). If ``None`` is given
    for ``name``, a path to the ``samples/`` directory will be returned.

    """

    data_dir = pkg_resources.resource_filename("dnasearch.tests", "data")
    if not os.path.exists(data_dir):
        raise RuntimeError("Could not retrieve data directory.")

    return data_dir
