import fortranformat as ff
from abc import ABC


class Values(ABC):
    """
    Abstract class to parse value lines from the ERRORR files.

    Parameters
    ----------
    lines : list
        list of value lines from the file

    Attributes
    ----------
    lines : list
        list of value lines from the file

    parsed_values : list
        list of the values in the section

    Methods
    -------
    parse_lines
        Parse the lines by their format string


    """

    def __init__(self, lines):
        self.lines = lines
        self.parse_lines()

    def parse_lines(self):
        """Parse the values lines by their format string

        Parameters
        ----------
        None

        Returns
        -------
        None, sets the attribute self.parsed_values

        """
        control_line = ff.FortranRecordReader("(6G11.0)")
        parsed_lines = [control_line.read(line) for line in self.lines]
        self.parsed_values = [item for line in parsed_lines for item in line]
