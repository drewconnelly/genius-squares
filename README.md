# genius-squares
A solver for the Genius Squares game

## Overview
This project provides a backtracking solver for the Genius Squares puzzle game, which involves placing 9 tetris-style pieces on a 6x6 board with some blocked cells.

## Scripts

### Main Solver
Solve a specific puzzle configuration with all pieces:
```bash
python play.py
```
This script:
- Defines the 9 game pieces (I, A, O, T, S, 1, 2, L, J)
- Sets blocked cells on the 6x6 board
- Finds and displays all solutions
- Shows colored output for easy visualization

### Quick Configuration Testing
Test specific blocked cell configurations:
```bash
python test_config.py
```
Tests predefined configurations and shows the number of solutions for each.

### Configuration Analysis
Find optimal blocked cell configurations:
```bash
python analyze_configurations.py
```
Analyzes multiple configurations to find ones with the fewest/most solutions.

### Quick Strategic Analysis
Test strategically interesting configurations:
```bash
python quick_analysis.py
```
Quickly tests corner-heavy, center-heavy, edge, diagonal, and scattered configurations.

### Constrained Testing
Test configurations with specific constraints:
```bash
python test_constrained.py
```

## Customization

### Modifying Blocked Cells
Edit the `false_cells` list in [play.py](play.py):
```python
false_cells = ['A6', 'E3', 'A1', 'A4', 'F2', 'F4', 'B2']
```

### Modifying Pieces
Edit the `PIECES` dictionary in [play.py](play.py) to change piece shapes:
```python
PIECES = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],  # 4-cell line
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],  # 2x2 square
    # ... add or modify pieces
}
```

## Requirements
- Python 3.x
- No external dependencies (uses only standard library)
