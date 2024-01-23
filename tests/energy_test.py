import pytest
import ENDFtk
from pathlib import Path
from pyerr import EnergyGroups

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file1 = mat.file(1)
    energy_groups = file1.section(451).content.split("\n")
    return energy_groups

def test_u235_endf81(u235_endf81):
    obj = EnergyGroups(u235_endf81)
    assert obj.MT == 451
    assert obj.group_boundaries[0] == 0.000139
    assert obj.num_boundaries == obj.num_groups + 1