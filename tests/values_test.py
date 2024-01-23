import pytest
import ENDFtk
from pathlib import Path
from pyerr.base import Values
from pyerr import EnergyGroupValues

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    return mat


def test_values_U235_ENDF81(u235_endf81):
    file1 = u235_endf81.file(1)
    energy_groups = file1.section(451)
    lines = energy_groups.content.split("\n")
    lines = lines[2:-2]
    obj = Values(lines)
    assert obj.parsed_values[0] == 0.000139
    assert obj.parsed_values[-1] == 0


def test_energies_U235_ENDF81(u235_endf81):
    file1 = u235_endf81.file(1)
    energy_groups = file1.section(451)
    lines = energy_groups.content.split("\n")
    lines = lines[2:-2]
    obj = EnergyGroupValues(lines,30)
    assert obj.parsed_values[0] == 0.000139
    assert obj.parsed_values[-1] == 17000000.0