import numpy as np
import pandas as pd
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

    lower_limit : float, optional, default is None
        the lower limit in energy (eV) to cut the values at. If not given, uses the lower 
        limit of the matrix in the file. If given, will cut out groups below the lower 
        limit. If the lower limit falls within a group, that group is kept


    upper_limit : float, optional, default is None
        the upper limit in energy (eV) to cut the values at. If not given, uses the upper 
        limit of the matrix in the file. If given, will cut out groups below the upper 
        limit. If the upper limit falls within a group, that group is kept

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
        Relative covariance matrix

    abs_covariance_matrix : np.array
        Absolute covariance matrix

    uncertainty : np.array
        The uncertainty values

    abs_uncertainty : np.array
        The absolute uncertainty values

    correlation_matrix : np.array
        Correlation matrix

    eig_values : np.array
        Sorted (largest to smallest) eigen values of the
        absolute covariance matrix

    eig_vectors : np.array
        Sorted (largest to smallest) eigen vectors of the
        absolute covariance matrix

    unc_convergence_table : pandas DataFrame
        pandas DataFrame with the absolute and relative difference
        between the overall uncertainty and the uncertainty of
        the covariance matrix reconstructed with k eigenvalues

    Methods
    -------
    get_correlation_matrix
        Function to get the uncertainty vector and correlation matrix

    get_eigenvalues
        Function to get sorted eigenvalues and eigenvectors
        of the absolute covariance matrix

    reconstruct_covariance 
        Function to reconstruct the covariance matrix from the 
        largest k eigenvalues

    get_pca_realizations
        Function to sample realizations by PCA, using the largest
        k components.

    quantify_uncertainty_convergence
        Function to quantify the convergence of the uncertainty 
        vector as more PCA eigenvalues are added
        
    """

    def __init__(self,energy_lines, mean_lines, covariance_lines, lower_limit=None, upper_limit=None):
        self._energy = EnergyGroups(energy_lines, lower_limit, upper_limit)
        self._mean = Mean(mean_lines, self._energy.indices)
        self._covariance = Covariance(covariance_lines,self._energy.control.num_groups, self._energy.indices)




        # check lengths
        assert len(self.mean_values) == len(self.group_boundaries) - 1
        assert len(self.mean_values) == len(self.covariance_matrix)

        self.get_correlation_matrix()
        self.get_eigenvalues()


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
        if self.MF == 5:    
            return self._mean.incident_energy
        else:
            return self._energy.group_boundaries

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
        self.abs_uncertainty = self.uncertainty * self.mean_values

        unc_mat = self.uncertainty*np.identity(len(self.uncertainty))
        
        self.correlation_matrix = np.linalg.inv(unc_mat)@self.covariance_matrix@np.linalg.inv(unc_mat).T

        # create the absolute covariance matrix from the absolute uncertainty
        abs_unc_mat = self.abs_uncertainty*np.identity(len(self.uncertainty))
        self.abs_covariance_matrix = abs_unc_mat@self.correlation_matrix@abs_unc_mat

    def get_eigenvalues(self):
        """ Function to get and sort eigenvalues and eigenvectors
            of the absolute covariance matrix """
        
        eig_vals,eig_vects = np.linalg.eigh(self.abs_covariance_matrix)

        # indices for sorting
        idx = eig_vals.argsort()[::-1]

        # sorted
        self.eig_vals = eig_vals[idx]
        self.eig_vects = eig_vects[:,idx]

    def reconstruct_covariance(self,k=None):
        """ Function to reconstruct the covariance matrix from the 
        largest k eigenvalues

        Parameters
        ----------
        k : int, optional, default is None
            the number of eigenvalues to use. If None, will use
            all of the eigenvalues of the covariane matrix

        Returns
        -------
        numpy array 
            The covariance matrix reconstructed from the top k
            eigenvalues

        """

        # set k to all of the eigen values if not given or greater
        # than the total number
        if k is None or k > len(self.eig_vals):
            k = len(self.eig_vals)

        # cut the top k 
        principle_eig_vals = self.eig_vals[:k]
        principle_eig_vects = self.eig_vects[:,:k]    

        # in Rising 2013, Equaton (10)
        return principle_eig_vals * principle_eig_vects @ principle_eig_vects.T
    
    def get_pca_realizations(self,num_samples,k=None):
        """ Function to sample realizations by PCA, using the largest
        k components.

        Parameters
        ----------
        num_samples : int
            The number of samples

        k : int, optional, default is None
            the number of eigenvalues to use. If None, will use
            all of the eigenvalues of the covariane matrix

        Returns
        -------
        numpy array
            the sampled realizations        
        
        """

        # set k to all of the eigen values if not given or greater
        # than the total number
        if k is None or k > len(self.eig_vals):
            k = len(self.eig_vals)

        # cut the top k 
        principle_eig_vals = self.eig_vals[:k]
        principle_eig_vects = self.eig_vects[:,:k]    

        # get samples
        gaussian_samples = np.random.normal(0,1,(k,num_samples))
        k_sum = np.sqrt(principle_eig_vals) * principle_eig_vects @ gaussian_samples

        # reshape the mean vector
        mean_vect = np.array(self.mean_values).reshape((len(self.mean_values),1))
        mean_vect = np.repeat(mean_vect, num_samples, axis=1)
        
        # Rising 2013 equation (7)
        realizations = mean_vect + k_sum

        # reshape realization
        return realizations.T


    def quantify_uncertainty_convergence(self):
        """ Function to quantify the convergence of the uncertainty vector
        as more PCA eigenvalues are added

        Parameters
        ----------
        None

        Returns
        -------
        None, creates the attribute unc_convergence_table
        
        """

        data = []
        print(len(self.eig_vals))
        for k in range(1,len(self.eig_vals)+1):
            cov = self.reconstruct_covariance(k)
            unc = np.sqrt(np.diag(cov))/self.mean_values

            abs_diff = self.uncertainty - unc
            rel_diff = abs_diff/self.uncertainty


            data.append([k,np.max(abs_diff),np.max(rel_diff)])

        self.unc_convergence_table = pd.DataFrame(data, 
                                                 columns=['k','abs_diff', 'rel_diff'],
                                                 )
        
