import pytest
import numpy as np
import ENDFtk
from pathlib import Path
from pyerr import ErrorrOutput

@pytest.fixture
def u235_endf81():
    filename = Path(__file__).parent / "files" / "u235_endf81.txt"
    return filename

def test_covergence_table_limit_low(u235_endf81):
    obj = ErrorrOutput(u235_endf81)
    pfns = obj.sections[18]
    pfns.quantify_uncertainty_convergence(e_min=11)
    print(pfns.unc_convergence_table.head())
    assert 'k' in pfns.unc_convergence_table.columns
    assert pfns.unc_convergence_table.rel_diff.iloc[-1] < 1e-4
    assert pfns.unc_convergence_table.rel_diff.iloc[0] > 0.99
    assert pfns.unc_convergence_table.rel_ind.iloc[0] == 597


def test_covergence_table(u235_endf81):
    obj = ErrorrOutput(u235_endf81)
    pfns = obj.sections[18]
    pfns.quantify_uncertainty_convergence(e_max=10e6)
    assert 'k' in pfns.unc_convergence_table.columns
    assert pfns.unc_convergence_table.rel_ind.iloc[0] == 1
    assert pfns.unc_convergence_table.rel_ind.iloc[4] == 0