from pyerr.base import  Control, Values
import fortranformat as ff
import numpy as np
import sys

class CovarianceControl(Control):
    """
    Class to parse covariance control lines from the ERRORR files. 

    Parameters
    ----------
    lines : list
        list of control lines from the file

    Attributes
    ----------
    lines : list
        list of control lines from the file

    ZA : int
        ZA of the material

    AWR : float
        atomic weight ratio of the material

    MAT : int
        Material number

    MF : int
        File number

    MT : int
        Section/reaction number

    parsed_values : list
        list of the values in the control line

    num_groups : int
        Number of energy groups

    MT1 : int
        if cross-reaction covariance, the other MT value


    Methods
    -------
    parse_lines
        Parse the control lines by their format string
    """

    def __init__(self,lines):
        super().__init__(lines)
        self.num_sections = self.parsed_values[15]
        self.MT1 = self.parsed_values[13]


class Covariance:
    """
    Class to parse the covariance section of the ERRORR file 

    Parameters
    ----------
    lines : list
        list of text lines in the section

    num_groups : int
        number of energy groups, which is size of the matrix

    indices : tuple
        indices for cutting at the upper and lower limits

    Attributes
    ----------
    control : CovarianceControl object
        parsed control lines object
    
    matrix : np.array
        2D covariance matrix

    Methods
    -------
    parse_section
        function to parse each individual set of values

    """

    def __init__(self,lines,num_groups, indices):
        self.control = CovarianceControl(lines[:2])
        self.matrix = np.zeros((num_groups,num_groups))

        cov_lines = lines[2:-2]

        for i in range(self.control.num_sections):
            if len(cov_lines) > 0:
                cov_lines = self.parse_section(cov_lines)

        # apply energy mask
        self.matrix = self.matrix[indices[0]:indices[1], indices[0]:indices[1]]

        self.check_covariance_matrix()
        

    def parse_section(self,lines):
        """
        function to parse each individual set of values

        Parameters
        ----------
        lines : list
            list of lines

        Returns
        -------
        lines
            the list of lines with the already-parsed lines popped off

        """
        section_cont = ff.FortranRecordReader('(2G11.0,4I11)')
        section_values = ff.FortranRecordReader('(6G11.0)')
        _, _, _, mt1_group, num_values, mt_group = section_cont.read(lines.pop(0))

        # number of lines to read
        num_lines = int(np.ceil(num_values/6))

        # read into list of lists
        values = [section_values.read(lines.pop(0)) for i in range(num_lines)]

        # flatten list
        values = [item for line in values for item in line]

        # cut zeros at the end of the list
        values = values[:num_values]

        # fill in matrix
        self.matrix[mt_group-1,mt1_group-1:mt1_group-1+num_values] = values

        return lines
    
    def check_covariance_matrix(self):
        """ function to check the covariance matrix for:
        
        - zeros on the diagonal (gracefully crash)
        
        """

        diagonal = np.diag(self.matrix)
        if np.min(diagonal) <= 0:
            print("Covariance matrix has zero and/or negative values along the diagonal. This may be caused by an inappropriate group structure chosen in NJOY - the original structure in the evaluation should be used instead.")
            print(len(diagonal))
            print(diagonal)
            sys.exit("Zeros on the diagonal.\n")
