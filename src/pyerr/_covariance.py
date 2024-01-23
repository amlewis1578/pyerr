from pyerr.base import  Control, Values
import fortranformat as ff

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
        self.num_groups = self.parsed_values[15]
        self.MT1 = self.parsed_values[13]