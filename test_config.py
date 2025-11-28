#!/usr/bin/env python3
"""
Simple tool to test false_cells configurations quickly.
"""

from geniusSquare import create_matrix, solve_puzzle

PIECES = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
    'A': [(0, 0), (0, 1), (0, 2)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 0), (0, 1), (0, 2), (1, 1)],
    'S': [(0, 1), (0, 2), (1, 0), (1, 1)],
    '1': [(0, 0)],
    '2': [(0, 0), (0, 1)],
    'L': [(0, 0), (0, 1), (1, 0)],
    'J': [(0, 0), (0, 1), (0, 2), (1, 0)],
}

def test_config(false_cells):
    """Test a configuration and return the number of solutions."""
    matrix = create_matrix(false_cells)
    solutions = solve_puzzle(matrix, PIECES, find_all=False)  # Find just one to see if solvable

    if not solutions:
        return 0

    # If solvable, find all solutions
    solutions = solve_puzzle(matrix, PIECES, find_all=True)
    return len(solutions)

if __name__ == "__main__":
    # Test a few key configurations
    configs = [
        (['A1', 'A3', 'A5', 'C5', 'D3', 'D5', 'F1'], "Current"),
        (['A1', 'A6', 'F1', 'F6', 'C3', 'D3', 'E3'], "Four corners + line"),
        (['C2', 'C3', 'C4', 'D2', 'D4', 'E2', 'E3'], "Center block"),
        (['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'C1'], "Diagonal"),
    ]

    for config, name in configs:
        try:
            count = test_config(config)
            print(f"{name}: {count} solutions")
        except Exception as e:
            print(f"{name}: ERROR - {e}")