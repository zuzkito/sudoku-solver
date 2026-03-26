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
```
sudoku-solver/ 
├── main.py # GUI application and user interface 
├── board.py # SudokuBoard class for board management 
├── solvers.py # Solving algorithms implementation 
└── images/ # Application icons and assets
```


### Core Modules

- **board.py**: Defines the `SudokuBoard` class with methods for:
  - Getting/setting cell values
  - Validating moves against Sudoku rules
  - Validating entire boards
  - Finding empty cells

- **solvers.py**: Contains three solving functions:
  - `solve_backtracking()`: Brute force recursive solver
  - `solve_constraint()`: Constraint propagation solver
  - `solve_combined()`: Hybrid solver using both approaches
  - Helper functions for possibility evaluation

- **main.py**: Full GUI implementation with:
  - Tkinter-based interface
  - Button controls (Solve, Validate, Clear)
  - Menu system (File, Solver selection, Samples, Help)
  - File I/O operations
  - Input validation

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- Pillow (PIL) for image handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zuzkito/sudoku-solver.git
cd sudoku-solver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
