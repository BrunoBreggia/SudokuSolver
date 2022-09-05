# -*- coding: utf-8 -*-
"""
Resuelvo sudokus mediante la estrategia de búsqueda heurística
denominada RECOCIDO SIMULADO ("simulated annealing")

Basado en el paper "Metaheuristics can solve sudoku puzzles"
de Rhyd Lewis (Springer, 2007)
"""

from sudoku import Sudoku
from simulated_annealing import SudokuSolver

filename = "sudoku1.csv"
sudoku = Sudoku.from_csv(filename)
print(sudoku)

solver = SudokuSolver()
solver(sudoku, showIter=True)
print(solver.sudoku)
solver.save_csv()

