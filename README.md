# Sudoku Solver

A Python-based Sudoku solver with a user-friendly GUI built using Tkinter. Solves puzzles using multiple algorithms and validates users own Sudoku boards. My first coding project for my introductory course in programming at uni.

## Features

- **Multiple Solving Algorithms**:
  - **Backtracking Bruteforce**: Classic recursive backtracking algorithm for guaranteed solutions
  - **Constraint Propagation**: Smart solver that uses logical deduction to identify cells with only one possible value
  - **Combined (Default)**: Hybrid approach that applies constraint propagation first, then uses backtracking for remaining cells

- **Interactive GUI** (SudOK):
  - 9x9 Sudoku grid with easy-to-use input fields
  - Real-time input validation (single digits only)
  - Solves puzzles and validates board against Sudoku rules
  - Sample puzzles to enable demo run of the app
  - Bonus easter egg content

- **File Management**:
  - Import/Export Sudoku puzzles from/to `.txt` files
  - Properly formatted file support for easy sharing, is also human readable


## Project Structure
