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
output = ErrorOutput(filename)
```

The `output` object has an attribute `output.section` which is a dictionary that contains `Section` objects for each MT in the file.

Each `Section` object has the following attributes:

    - MAT : the material numbers
    - MF : the MF number that the mean values came from 
    - MT : the MT number for the reaction
    - incident_energy : the incident energy at which the processing was done (in eV)
    - num_groups : the number of energy groups
    - group_boundaries : the boundaries of the energy groups, in eV
    - mean_values : mean values for the reaction specified
    - covariance_matrix : np.array of the covariance matrix
    - correlation_matrix : np.array of the correlation matrix
    - uncertainty : np.array of the uncertainty values 