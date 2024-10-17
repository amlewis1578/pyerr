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
def u235_endf81_30():
    filename = Path(__file__).parent / "files" / "u235_endf81_30.txt"
    return filename


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
    assert len(obj.sections[452].mean_values) == len(obj.sections[452].uncertainty)
    assert len(obj.sections[452].mean_values) == len(obj.sections[452].group_boundaries) - 1


def test_U235_wrong_grouping(u235_endf81_30):
    with pytest.raises(SystemExit):
        ErrorrOutput(u235_endf81_30)


def test_U235(u235_endf81):
    obj = ErrorrOutput(u235_endf81)
    assert np.isclose(obj.sections[18].abs_covariance_matrix[0, 0], 1.06828e-19)


def test_energy_boundaries(u235_endf81):
    obj = ErrorrOutput(u235_endf81, upper_limit=28850000)
    assert len(obj.sections[18].group_boundaries) == 641 - 4

    obj = ErrorrOutput(u235_endf81, upper_limit=28800000)
    assert len(obj.sections[18].group_boundaries) == 641 - 5

    obj = ErrorrOutput(u235_endf81, lower_limit=11.5, upper_limit=28800000)
    assert len(obj.sections[18].group_boundaries) == 641 - 5 - 2

    obj = ErrorrOutput(u235_endf81, lower_limit=10, upper_limit=28800000)
    assert len(obj.sections[18].group_boundaries) == 641 - 5 - 1

    # check bounds outside the region - should just default to the whole region
    obj = ErrorrOutput(u235_endf81, lower_limit=-10, upper_limit=5e7)
    assert len(obj.sections[18].group_boundaries) == 641
