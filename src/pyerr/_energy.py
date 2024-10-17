from pyerr.base import Control, Values
import numpy as np


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

    temperature : float
        temperature at which the evaluation was processed

    num_groups : int
        Number of energy groups

    num_boundaries : int
        Number of energy group boundaries (num_groups + 1)

    Methods
    -------
    parse_lines
        Parse the control lines by their format string
    """

    def __init__(self, lines):
        super().__init__(lines)
        self.temperature = self.parsed_values[10]
        self.num_groups = self.parsed_values[12]
        self.num_boundaries = np.array(self.parsed_values[14])


class EnergyGroupValues(Values):
    """
    Class to parse energy group boundaries

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

    def __init__(self, lines, num_values):
        super().__init__(lines)
        self.num_values = num_values
        self.parsed_values = np.array(self.parsed_values[: num_values + 1])


class EnergyGroups:
    """
    Class to parse energy group section of the ERRORR file, in MF1MT451

    Parameters
    ----------
    lines : list
        list of lines in MF1MT451

    lower_limit : float or None
        lower limit, in eV, to cut the values at. If None or if the value is
        outside the range, no cut is made at the low end

    upper_limit : float or None
        upper limit, in eV, to cut the values at. If None or if the value is
        outside the range, no cut is made at the high end


    Attributes
    ----------
    control : EnergyGroupControl object
        parsed control lines object

    values : EnergyGroupValues object
        parsed values lines object

    indices : tuple
        indices for cutting at the upper and lower limits

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

    temperature : float
        temperature at which the evaluation was processed

    """

    def __init__(self, lines, lower_limit, upper_limit):
        self.control = EnergyGroupControl(lines[:2])
        self.values = EnergyGroupValues(lines[2:-2], self.control.num_groups)
        if upper_limit is None or upper_limit > np.max(self.values.parsed_values):
            upper_limit = np.max(self.values.parsed_values)
        if lower_limit is None or lower_limit < np.min(self.values.parsed_values):
            lower_limit = np.min(self.values.parsed_values)

        # get the upper and lower indices
        #    if limit falls within a group, keep that group
        lower_ind = np.where(self.values.parsed_values <= lower_limit)[0][-1]
        upper_ind = np.where(self.values.parsed_values >= upper_limit)[0][0]
        self.indices = (lower_ind, upper_ind)

    @property
    def group_boundaries(self):
        return self.values.parsed_values[self.indices[0] : self.indices[1] + 1]

    @property
    def num_boundaries(self):
        return len(self.group_boundaries)

    @property
    def num_groups(self):
        return len(self.group_boundaries) - 1

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

    @property
    def temperature(self):
        return self.control.temperature
