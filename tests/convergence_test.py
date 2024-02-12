import pytest
import numpy as np
import ENDFtk
from pathlib import Path
from pyerr import ErrorrOutput

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    return filename

def test_covergence_table(u235_endf81):
    obj = ErrorrOutput(u235_endf81)
    pfns = obj.sections[18]
    pfns.quantify_uncertainty_convergence()
    assert 'k' in pfns.unc_convergence_table.columns
    assert pfns.unc_convergence_table.rel_diff.iloc[-1] < 1e-4
    assert pfns.unc_convergence_table.rel_diff.iloc[0] > 0.99
