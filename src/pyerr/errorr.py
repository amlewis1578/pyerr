import numpy as np
import ENDFtk
from pyerr import Section

class ErrorrOutput:
    """
    Class to hold a full ERRORR output, with multiple sections 

    Parameters
    ----------
    filename : str
        the ERRORR output file name

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
    filename : str
        the ERRORR output file name

    sections : dictionary
        Dictionary of Section classes, one for each MT value

    Methods
    -------
    open_errorr_file
        Function to parse the ERRORR file with ENDFtk
    
    """

    def __init__(self,filename,lower_limit=None, upper_limit=None):
        self.filename = filename
        section_numbers = self.open_errorr_file()

        # create Section class for each
        self.sections = {}
        for mf, mt in section_numbers:
            energy_lines = self._mat.file(1).section(451).content.split("\n")
            mean_lines = self._mat.file(mf).section(mt).content.split("\n")
            cov_lines = self._mat.file(mf+30).section(mt).content.split("\n")
            self.sections[mt] = Section(energy_lines, mean_lines, cov_lines, lower_limit, upper_limit)


    def open_errorr_file(self):
        """ Function to parse the ERRORR file with ENDFtk """
        tape = ENDFtk.tree.Tape.from_file(str(self.filename))
        mat_num = tape.material_numbers[0]
        self._mat = tape.material(mat_num)

        list_of_mfs = self._mat.file_numbers.to_list()

        # check that File 1 is there
        assert 1 in list_of_mfs

        section_numbers = []
        
        if 3 in list_of_mfs:
            for mt in self._mat.file(3).section_numbers:
                section_numbers.append((3,mt))
        
        if 5 in list_of_mfs:
            for mt in self._mat.file(5).section_numbers:
                section_numbers.append((5,mt))

        return section_numbers
