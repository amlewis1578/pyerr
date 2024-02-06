# pyerr
python package to parse ERRORR output files

## installation

This package requires the LANL python package ![ENDFtk](https://github.com/njoy/ENDFtk)

To install `pyerr`, move into the directory and run

```bash
pip install .
```

## use

The main user class in `pyerr` is the `ErrorOutput` class. It takes in the path to an ERRORR output file

```python
from pyerr import ErrorOutput

filename = "tape28"
output = ErrorOutput(filename,lower_limit=1e5, upper_limit=2e7)
```

The arguments `lower_limit` and `upper_limit` are optional, with default values of `None`. If given, they are each floats in eV and the values are cut at those values. If the limits fall within a group, the group is kept.
 
The `output` object has an attribute `output.section` which is a dictionary that contains `Section` objects for each MT in the file.

Each `Section` object has the following attributes:

- `MAT` : the material numbers
- `MF` : the MF number that the mean values came from 
- `MT` : the MT number for the reaction
- `incident_energy` : for PFNS, the incident energy at which the processing was done (in eV). For nu-bar or cross section, returns the list of group boundaries
- `num_groups` : the number of energy groups
- `group_boundaries` : the boundaries of the energy groups, in eV
- `mean_values` : mean values for the reaction specified
- `covariance_matrix` : np.array of the relative covariance matrix
- `correlation_matrix` : np.array of the correlation matrix
- `uncertainty` : np.array of the relative uncertainty values 
- `abs_uncertainty` : np.array of the absolute uncertainty values 
- `abs_covariance` : np.array of the absolute covariance matrix
- `eig_vals` : np.array of sorted eigenvalues
- `eig_vects` : np.array of sorted eigenvectors

and the following user methods:

- `reconstruct_covariance(k)` : given the number of principle eigenvalues, k, reconstructs the covariance matrix
- `get_pca_realizations(num_samples, k)` : given the number of samples and the number of principal components (eigenvalues), k, produce sample realizations


## details

When running NJOY to get the covariance matrix, the default option to produce a relative covariance matrix should be chosen. There is not a good way to check that this option was chosen (except the OOM of the values) so it is assumed that the covariance is relative when reading.