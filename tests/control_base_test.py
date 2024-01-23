import pytest
import ENDFtk
from pathlib import Path
from pyerr.base import Control

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    return mat

def test_control_U235_ENDF81(u235_endf81):
    file1 = u235_endf81.file(1)
    energy_groups = file1.section(451)
    lines = energy_groups.content.split("\n")
    control_lines = lines[:2]
    obj = Control(control_lines)
    assert obj.ZA == 92235
    assert obj.MT == 451