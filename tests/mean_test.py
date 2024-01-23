import pytest
import ENDFtk
from pathlib import Path
from pyerr._mean import MeanControl

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file5 = mat.file(5)
    lines = file5.section(18).content.split("\n")
    return lines


def test_u235_endf81(u235_endf81):
    print(u235_endf81[0])
    obj = MeanControl(u235_endf81[0])
    assert obj.incident_energy == 2.5e5
    assert obj.parsed_values[4] == 30
    assert obj.MT == 18