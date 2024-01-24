import pytest
import numpy as np
import ENDFtk
from pathlib import Path
from pyerr import Section


@pytest.fixture
def nubar_test_file():
    filename = Path(__file__).parent / "files" / "nubar_example.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file1 = mat.file(1)
    file3 = mat.file(3)
    file33 = mat.file(33)
    return file1, file3, file33

@pytest.fixture
def nubar_test_452(nubar_test_file):
    file1, file3, file33 = nubar_test_file
    energy_lines = file1.section(451).content.split("\n")
    mean_lines = file3.section(452).content.split("\n")
    cov_lines = file33.section(452).content.split("\n")
    return energy_lines, mean_lines, cov_lines

@pytest.fixture
def nubar_452_matrix():
    filename = Path(__file__).parent / "files" / "nubar_example_matrix.npy"
    return np.load(filename)

def test_nubar_452(nubar_test_452, nubar_452_matrix):
    obj = Section(*nubar_test_452)
    assert obj.group_boundaries[0] == 1.390000e-4
    assert obj.mean_values[0] == 2.487540
    assert obj.covariance_matrix[0,0] == 2.996458e-4
    assert obj.covariance_matrix[28,28] == 2.530043e-4
    assert obj.covariance_matrix[29,0] == 9.161621e-6
    assert np.array_equal(obj.covariance_matrix, nubar_452_matrix)