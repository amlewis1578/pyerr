import pytest
import ENDFtk
from pathlib import Path
from pyerr._covariance import CovarianceControl

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file35 = mat.file(35)
    lines = file35.section(18).content.split("\n")
    return lines

def test_u235_endf81_control(u235_endf81):
    obj = CovarianceControl(u235_endf81[:2])
    assert obj.MT == 18
    assert obj.MT1 == 18
    assert obj.ZA == 92235
