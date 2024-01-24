import numpy as np
from pyerr import EnergyGroups, Mean, Covariance

class Section:
    """
    Class to hold a single section (MT value) from an ERRORR file, which includes
    the energy grid, the mean value, and the covariance matrix

    Parameters
    ----------
    energy_lines : list
        list of the lines from the file corresponding to the energy grid

    mean_lines : list
        list of the lines from the file corresponding to the mean values

    covariance_lines : list
        list of the lines from the file corresponding to the covariance

    Attributes
    ----------
    MAT : int
        Material number

    MF : int
        File number

    MT : int
        Section/reaction number

    incident_energy : float
        Incident energy in eV

    num_groups : int
        Number of energy groups
        
    group_boundaries : int
        Boundaries of the energy groups

    mean_values : list
        Mean values of the quantity

    covariance_matrix : np.array
        Covariance matrix

    Methods
    -------
    get_correlation_matrix
        Function to get the uncertainty vector and correlation matrix
    """

    def __init__(self,energy_lines, mean_lines, covariance_lines):
        self._energy = EnergyGroups(energy_lines)
        self._mean = Mean(mean_lines)
        self._covariance = Covariance(covariance_lines,self._energy.num_groups)

        self.get_correlation_matrix()


    @property
    def MAT(self):
        return self._mean.MAT
    
    @property
    def MF(self):
        return self._mean.MF
    
    @property
    def MT(self):
        return self._mean.MT
    
    @property
    def incident_energy(self):
        return self._mean.incident_energy

    @property
    def group_boundaries(self):
        return self._energy.group_boundaries

    @property
    def num_groups(self):
        return self._energy.num_groups
    
    @property
    def mean_values(self):
        return self._mean.values
    
    @property
    def covariance_matrix(self):
        return self._covariance.matrix
    
    def get_correlation_matrix(self):
        """ Function to get the uncertainty vector and correlation matrix """
        self.uncertainty = np.sqrt(np.diag(self.covariance_matrix))
        
        unc_mat = self.uncertainty*np.identity(len(self.uncertainty))
        
        self.correlation_matrix = np.linalg.inv(unc_mat)@self.covariance_matrix@np.linalg.inv(unc_mat).T
