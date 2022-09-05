# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

class Sudoku:
    
    def __init__(self):
        self._content = []
        self._original_content = []
    
    @classmethod
    def from_string(cls, string):
        """
        Loads sudoku from string
        """
        sudoku = cls()
        sudoku.content = np.array( [ [int(i) for i in line] 
                                    for line in string.split() ] )
        return sudoku
    
    @classmethod
    def from_csv(cls, filename):
        """
        Loads sudoku from csv file (comma separated value file)
        """
        sudoku = cls()
        df = pd.read_csv(filename, header=None)
        sudoku.content = df.to_numpy()
        return sudoku
    
    def to_csv(self, filename):
        """
        Loads sudoku to csv file (comma separated value file)
        """
        pd.DataFrame(self._content).to_csv(filename,
                                           header=None,
                                           index =None)
    
    @property
    def content(self):
        return self._content
        # return self.get_string()
    
    @property
    def original_content(self):
        return self._original_content
        # return self.get_string(original=True)
    
    @content.setter
    def content(self, new_content):
        # accepted input must be generalized...
        if new_content.shape != (9,9):
            raise ValueError("Expected 9x9 numpy array")
        self._original_content = new_content.copy()
        self._content = new_content.copy()
    
    def __getitem__(self, pos):
        if type(pos) is int:
            # returns a whole square
            return self._content[(pos//3)*3:(pos//3+1)*3,
                                 (pos% 3)*3:(pos% 3+1)*3]
        elif len(pos) == 2:
            return self._content[pos]
        elif len(pos) == 3:
            # first element is square, second and third row & column
            global_row_index = (pos[0]//3)*3 + pos[1]
            global_col_index = (pos[0]% 3)*3 + pos[2]
            return self._content[global_row_index, global_col_index]
        else:
            raise IndexError("Not a valid matrix position")
    
    def __setitem__(self, pos, value):
        if len(pos) == 2:
            if self._original_content[pos] != 0:
                raise IndexError("Cant override original number")
            self._content[pos] = value
        elif len(pos) == 3:
            # first element is square, second and third row & column
            global_ridx = (pos[0]//3)*3 + pos[1]
            global_cidx = (pos[0]% 3)*3 + pos[2]
            if self._original_content[global_ridx, global_cidx] != 0:
                raise IndexError("Cant override original number")
            self._content[global_ridx, global_cidx] = value
        else:
            raise IndexError("Not a valid matrix position")
        
    def number_of_errors(self):
        """
        Applies cost function to sudoku as is
        """
        numberOfErrors = 0 
        for i in range (0,9):
            numberOfErrors += (9 - len(np.unique(self[:,i]))) 
            numberOfErrors += (9 - len(np.unique(self[i,:])))
        return numberOfErrors
    
    def get_string(self, original=False):
        content = self._content if not original else self._original_content
        
        output = "\n"
        for i in range(len(content)):
            line = ""
            if i == 3 or i == 6:
                output += "---------------------\n"
            for j in range(len(content[i])):
                if j == 3 or j == 6:
                    line += "| "
                line += str(content[i,j])+" "
            output += line+'\n'
            
        return output
    
    def __str__(self):
        return self.get_string()
    
    def __repr__(self):
        return str(self)
    
if __name__ == '__main__':
    
    startingSudoku = """
                    024007000
                    600000000
                    003680415
                    431005000
                    500000032
                    790000060
                    209710800
                    040093000
                    310004750
                """

    s1 = Sudoku.from_string(startingSudoku)
    print(s1)
    
    filename = "sudoku1.csv"
    s2 = Sudoku.from_csv(filename)
    print(s2)
    
    
    