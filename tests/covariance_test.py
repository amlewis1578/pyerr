import pytest
import ENDFtk
import numpy as np
from pathlib import Path
from pyerr._covariance import CovarianceControl, Covariance

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file35 = mat.file(35)
    lines = file35.section(18).content.split("\n")
    return lines

@pytest.fixture
def u235_endf81_matrix():
    filename = Path(__file__).parent / "files" / "u235_endf81_matrix.npy"
    return np.load(filename)
    

def test_u235_endf81_control(u235_endf81):
    obj = CovarianceControl(u235_endf81[:2])
    assert obj.MT == 18
    assert obj.MT1 == 18
    assert obj.ZA == 92235
    assert obj.num_sections == 640


def test_u235_endf81(u235_endf81, u235_endf81_matrix):
    obj = Covariance(u235_endf81,640)
    assert obj.matrix[0,0] == 4.237122e-2
    assert np.array_equal(u235_endf81_matrix,obj.matrix)