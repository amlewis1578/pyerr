import pytest
import ENDFtk
from pathlib import Path
import numpy as np
from pyerr._mean import MeanControl, MeanValues, Mean


@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81_30.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file5 = mat.file(5)
    lines = file5.section(18).content.split("\n")
    return lines


def test_u235_endf81(u235_endf81):
    obj = MeanControl(u235_endf81[0])
    assert obj.incident_energy == 2.5e5
    assert obj.parsed_values[4] == 30
    assert obj.MT == 18


def test_u235_endf81(u235_endf81):
    obj = MeanValues(u235_endf81[1:-2], 30)
    assert obj.parsed_values[0] == 2.67762e-11
    assert obj.parsed_values[-1] == 3.564233e-5
    assert np.isclose(np.sum(obj.parsed_values), 1.0)


def test_u235_endf81(u235_endf81):
    obj = Mean(u235_endf81, (0, 30))
    assert obj.MT == 18
    assert obj.num_groups == 30
    assert obj.incident_energy == 2.5e5
    assert obj.values[0] == 2.67762e-11
