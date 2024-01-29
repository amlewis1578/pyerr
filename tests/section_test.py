import pytest
import numpy as np
import ENDFtk
from pathlib import Path
from pyerr import Section
import matplotlib.pyplot as plt


@pytest.fixture
def nubar_test_file():
    filename = Path(__file__).parent / "files" / "nubar_example.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file1 = mat.file(1)
    file3 = mat.file(3)
    file33 = mat.file(33)
    return file1, file3, file33

@pytest.fixture
def nubar_test_452(nubar_test_file):
    file1, file3, file33 = nubar_test_file
    energy_lines = file1.section(451).content.split("\n")
    mean_lines = file3.section(452).content.split("\n")
    cov_lines = file33.section(452).content.split("\n")
    return energy_lines, mean_lines, cov_lines

@pytest.fixture
def nubar_452_matrix():
    filename = Path(__file__).parent / "files" / "nubar_example_matrix.npy"
    return np.load(filename)


def test_nubar_452(nubar_test_452, nubar_452_matrix):
    obj = Section(*nubar_test_452)
    assert obj.group_boundaries[0] == 1.390000e-4
    assert obj.mean_values[0] == 2.487540
    assert obj.covariance_matrix[0,0] == 2.996458e-4
    assert obj.covariance_matrix[28,28] == 2.530043e-4
    assert obj.covariance_matrix[29,0] == 9.161621e-6
    assert np.array_equal(obj.covariance_matrix, nubar_452_matrix)
    assert obj.correlation_matrix[2,2] == 1.0
    assert np.array_equal(np.sqrt(np.diag(nubar_452_matrix)),obj.uncertainty)
    assert np.array_equal(obj.eig_vals,sorted(obj.eig_vals,reverse=True))


@pytest.fixture
def endf71_pfns_test_file():
    filename = Path(__file__).parent / "files" / "u235_endf71.txt"
    tape = ENDFtk.tree.Tape.from_file(str(filename))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file1 = mat.file(1)
    file5 = mat.file(5)
    file35 = mat.file(35)
    return file1, file5, file35

@pytest.fixture
def endf71_pfns(endf71_pfns_test_file):
    file1, file5, file35 = endf71_pfns_test_file
    energy_lines = file1.section(451).content.split("\n")
    mean_lines = file5.section(18).content.split("\n")
    cov_lines = file35.section(18).content.split("\n")
    return energy_lines, mean_lines, cov_lines

@pytest.fixture
def endf71_eigs():
    file_loc = Path(__file__).parent / "files" 
    return np.load(file_loc/"u235_endf71_eigvals.npy"),np.load(file_loc/"u235_endf71_eigvects.npy")

def test_endf71_pca(endf71_pfns,endf71_eigs):
    obj = Section(*endf71_pfns)
    assert np.array_equal(obj.eig_vals,sorted(obj.eig_vals,reverse=True))
    assert np.allclose(obj.eig_vals, endf71_eigs[0])
    # check the 20 largest, which are the relevant ones
    assert np.allclose(np.abs(obj.eig_vects[:,:20]), np.abs(endf71_eigs[1][:,:20]))

    # check that with all eigenvalues included, reconst cov is the same
    recon = obj.reconstruct_covariance()
    assert np.allclose(recon, obj.abs_covariance_matrix)

    # in this case, only 2 are needed to pretty much entirely reconstruct the cov mat
    recon = obj.reconstruct_covariance(2)
    assert np.allclose(recon, obj.abs_covariance_matrix)

    realizations = obj.get_pca_realizations(10,100)
    assert np.array_equal(realizations.shape, (10,275))
