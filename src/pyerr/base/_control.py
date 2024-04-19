import fortranformat as ff
from abc import ABC

class Control(ABC):
    """
    Abstract class to parse control lines from the ERRORR files. 

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

    Methods
    -------
    parse_lines
        Parse the control lines by their format string


    """
    def __init__(self,lines):
        self.lines = lines
        self.parse_lines()
        self.ZA = self.parsed_values[0]
        self.AWR = self.parsed_values[1]
        self.MAT = self.parsed_values[6]
        self.MF = self.parsed_values[7]
        self.MT = self.parsed_values[8]

    def parse_lines(self):
        """ Parse the control lines by their format string 
        
        Parameters
        ----------
        None

        Returns
        -------
        None, sets the attribute self.parsed_values

        """
        control_line = ff.FortranRecordReader('(2G11.0,4I11,I4,I2,I3,I5)')
        parsed_lines = [control_line.read(line) for line in self.lines]
        self.parsed_values = [item for line in parsed_lines for item in line]