from pyerr.base import Control, Values


class EnergyGroupControl(Control):
    """
    Class to parse energy group control lines from the ERRORR files. 

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

    num_boundaries : int
        Number of energy group boundaries (num_groups + 1)

    Methods
    -------
    parse_lines
        Parse the control lines by their format string
    """

    def __init__(self,lines):
        super().__init__(lines)
        self.num_groups = self.parsed_values[12]
        self.num_boundaries = self.parsed_values[14]


class EnergyGroupValues(Values):
    """
    Class to parse energy group boundaries  

    Parameters
    ----------
    lines : list
        list of control lines from the file

    num_values : int
        Number of values in the list, so that zeros at the
        end of the list can be removed

    Attributes
    ----------
    lines : list
        list of control lines from the file

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


class EnergyGroups:
    """
    Class to parse energy group section of the ERRORR file, in MF1MT451  

    Parameters
    ----------
    lines : list
        list of lines in MF1MT451

    Attributes
    ----------
    control : EnergyGroupControl object
        parsed control lines object

    values : EnergyGroupValues object
        parsed values lines object

    group_boundaries : list
        list of group boundaries

    num_boundaries : int
        number of group boundaries

    num_groups : int
        Number of groups (num_boundaries - 1)

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
        
    """


    def __init__(self,lines):
        self.control = EnergyGroupControl(lines[:2])
        self.values = EnergyGroupValues(lines[2:-2],self.control.num_groups)

    @property
    def group_boundaries(self):
        return self.values.parsed_values
    
    @property
    def num_boundaries(self):
        return self.control.num_boundaries
    @property
    def num_groups(self):
        return self.control.num_groups
    
    @property
    def ZA(self):
        return self.control.ZA  
    
    @property
    def AWR(self):
        return self.control.AWR 
        
    @property
    def MAT(self):
        return self.control.MAT 

    @property
    def MF(self):
        return self.control.MF 

    @property 
    def MT(self):
        return self.control.MT  

