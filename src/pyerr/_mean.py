from pyerr.base import  Values
import fortranformat as ff


class MeanControl:
    """
    Class to parse mean values control lines from the ERRORR files. 

    For some reason this section does not have the first control line,
    so the Control base class is not used

    Parameters
    ----------
    lines : list
        list of control lines from the file

    Attributes
    ----------
    lines : list
        list of control lines from the file

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

    incident_energy : float
        Incident energy in eV


    Methods
    -------
    parse_lines
        Parse the control lines by their format string
    """

    def __init__(self,line):
        self.line = line
        self.parse_line()
        self.incident_energy = self.parsed_values[1]
        self.num_groups = self.parsed_values[4]
        self.MAT = self.parsed_values[6]
        self.MF = self.parsed_values[7]
        self.MT = self.parsed_values[8]
        self.parsed_values = self.parsed_values[:self.num_groups+1]

    def parse_line(self):
        """ Parse the control line by its format string 
        
        Parameters
        ----------
        None

        Returns
        -------
        None, sets the attribute self.parsed_values

        """
        control_line = ff.FortranRecordReader('(2G11.0,4I11,I4,I2,I3,I5)')
        self.parsed_values = control_line.read(self.line)


class MeanValues(Values):
    """
    Class to parse mean values 

    Parameters
    ----------
    lines : list
        list of value lines from the file

    num_values : int
        Number of values in the list, so that zeros at the
        end of the list can be removed

    Attributes
    ----------
    lines : list
        list of value lines from the file

    num_values : int
        Number of values in the list, so that zeros at the
        end of the list can be removed

    parsed_values : list
        list of the values in the section, with zeros at the
        end of the list removed

    Methods
    -------
    parse_lines
        Parse the lines by their format string


    """
    def __init__(self,lines,num_values):
        super().__init__(lines)
        self.num_values = num_values
        self.parsed_values = self.parsed_values[:num_values+1]
