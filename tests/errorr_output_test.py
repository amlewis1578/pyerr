import pytest
import numpy as np
import ENDFtk
from pathlib import Path
from pyerr import ErrorrOutput

@pytest.fixture
def nubar_test_file():
    filename = Path(__file__).parent / "files" / "nubar_example.txt"
    return filename

@pytest.fixture
def nubar_452_matrix():
    filename = Path(__file__).parent / "files" / "nubar_example_matrix.npy"
    return np.load(filename)

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    return filename

def test_nubar(nubar_test_file, nubar_452_matrix):
    obj = ErrorrOutput(nubar_test_file)
    assert 452 in obj.sections.keys()
    assert 455 in obj.sections.keys()
    assert 456 in obj.sections.keys()
    assert np.array_equal(obj.sections[452].covariance_matrix, nubar_452_matrix)

