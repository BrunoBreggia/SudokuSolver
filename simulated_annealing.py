# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 01:55:04 2022

@author: Windows
"""

from sudoku import Sudoku
import pandas as pd
from copy import deepcopy
import numpy as np

class SimulatedAnnealing:
    """
    Simulated annealing metaheuristic searching method.
    Empty base class for inheritance.
    """
    pass


class SudokuSolver(SimulatedAnnealing):
    """
    A sudoku solver that employs simulating annealing approach
    to solve sudokus (instances of Sudoku class).
    """
    
    def __init__(self, init_temp=50, cool_rate=0.99, iter_per_T=30):
        self.initial_temperature = init_temp
        self.cooling_rate = cool_rate # between 0 and 1
        self.iterations = iter_per_T
    
    def __call__(self, sudoku:Sudoku, showIter=False):
        self.sudoku = sudoku
        self.nextState = None
        self.filling()
        cost = self.calculate_total_cost()
        print(cost)
        temperature = self.initial_temperature
        counter = 0
        while cost > 0:
            # generate candidate state
            delta = self.swap()
            
            # update probability
            if temperature > 0.01:
                prob = np.exp(-delta/temperature)
            else:
                prob = 0
                
            # determine if we swap states
            if delta < 0 or np.random.random() < prob:
                cost += delta
                self.sudoku = self.nextState
                
            # update temperature
            if counter == self.iterations:
                counter = 0
                temperature *= self.cooling_rate
            else:
                counter += 1
            
            if showIter: print(cost)
                
    
    def filling(self):
        """
        Fills all the blank spaces in the sudoku (positions with 0).
        Filled in such a way that we have all digits from 1 to 9
        in each square.
        """
        for sq in range(9):
            # determine numbers missing in the square
            used = np.unique(self.sudoku[sq])
            missing = np.array( [ num for num in range(1,10) 
                                 if num not in used] )
            np.random.shuffle(missing)
            
            # filling blank spaces randomly with the missing digits
            positions_to_fill = np.array(np.where(self.sudoku[sq] == 0)).T
            for i, (row, col) in enumerate(positions_to_fill):
                self.sudoku[sq,row,col] = missing[i]

    def swap(self):
        """
        Swaps the digits in two non-fixed cells from the same square,
        positions to swap determined randomly.
        Returns the veriation in the cost of the resulting sudoku.
        """
        # first cell to swap
        swap_positions = np.array(np.where(self.sudoku.original_content == 0)).T
        pos1 = swap_positions[np.random.choice(len(swap_positions))]
        pos1 = tuple(pos1) # positions must be tuples
        partial_cost = self.row_cost(pos1[0]) + self.col_cost(pos1[1])
        
        # second cell to swap
        sq = (pos1[0]//3)*3 + pos1[1]//3
        sq_swap_pos = [ p for p in swap_positions 
                        if  (sq//3)*3 <= p[0] < (sq//3+1)*3 
                        and (sq% 3)*3 <= p[1] < (sq% 3+1)*3 ]
        pos2 = sq_swap_pos[np.random.choice(len(sq_swap_pos))]
        pos2 = tuple(pos2) # positions must be tuples
        partial_cost += self.row_cost(pos2[0]) + self.col_cost(pos2[1])
        
        # swap
        self.nextState = deepcopy(self.sudoku)
        item1, item2 = self.nextState[pos1], self.nextState[pos2]
        self.nextState[pos1] = item2
        self.nextState[pos2] = item1
        
        # calculate cost variation
        partial_cost = -partial_cost
        partial_cost += self.row_cost(pos1[0], self.nextState) \
                        + self.col_cost(pos1[1], self.nextState)
        partial_cost += self.row_cost(pos2[0], self.nextState) \
                        + self.col_cost(pos2[1], self.nextState)
        
        return partial_cost
    
    def calculate_total_cost(self):
        """
        Cost defined as amount of digits missing in each row and 
        column (summed)
        """
        cost = 0 
        for i in range(0,9):
            cost += (9 - len(np.unique(self.sudoku[:,i]))) 
            cost += (9 - len(np.unique(self.sudoku[i,:])))
        return cost
    
    def row_cost(self, row, state=None):
        """
        Amount of digits missing in given row
        """
        if state is None:
            state = self.sudoku
        cost = 9 - len(np.unique(state[row,:]))
        return cost
    
    def col_cost(self, col, state=None):
        """
        Amount of digits missing in given column
        """
        if state is None:
            state = self.sudoku
        cost = 9 - len(np.unique(state[:,col]))
        return cost
    
    def save_csv(self, filename="solved_sudoku.csv"):
        self.sudoku.to_csv(filename)
        
if __name__ == '__main__':
    
    filename = "sudoku1.csv"
    sudoku = Sudoku.from_csv(filename)
    print(sudoku)
    
    solver = SudokuSolver()
    solver(sudoku)
    solver.save_csv()
    
