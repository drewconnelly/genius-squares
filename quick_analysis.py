#!/usr/bin/env python3
"""
Quick analysis of strategic false_cells configurations.
"""

from geniusSquare import create_matrix, solve_puzzle

PIECES = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],          # I-piece (4 cells)
    'A': [(0, 0), (0, 1), (0, 2)],                  # A-piece (3 cells)
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],          # O-piece (4 cells, square)
    'T': [(0, 0), (0, 1), (0, 2), (1, 1)],          # T-piece (4 cells)
    'S': [(0, 1), (0, 2), (1, 0), (1, 1)],          # S-piece (4 cells)
    '1': [(0, 0)],                                  # one-piece (1 cell)
    '2': [(0, 0), (0, 1)],                          # two-piece (2 cells)
    'L': [(0, 0), (0, 1), (1, 0)],                  # L-piece (3 cells)
    'J': [(0, 0), (0, 1), (0, 2), (1, 0)],          # J-piece (4 cells)
}

def test_configuration(false_cells, name=""):
    """Test a single configuration quickly."""
    try:
        matrix = create_matrix(false_cells)
        solutions = solve_puzzle(matrix, PIECES, find_all=True)
        print(f"{name:25} {str(false_cells):50} -> {len(solutions):3d} solutions")
        return len(solutions)
    except Exception as e:
        print(f"{name:25} {str(false_cells):50} -> ERROR: {e}")
        return None

def main():
    """Test strategic configurations."""
    print("Configuration Name        False Cells                                        Solutions")
    print("-" * 85)

    # Current configuration
    test_configuration(['A1', 'A3', 'A5', 'C5', 'D3', 'D5', 'F1'], "Current")

    # Corner-heavy configurations (harder to fill)
    test_configuration(['A1', 'A6', 'F1', 'F6', 'C3', 'C4', 'D4'], "All corners + center")
    test_configuration(['A1', 'A2', 'A6', 'F1', 'F6', 'C3', 'D3'], "Corner clusters")

    # Center-heavy configurations
    test_configuration(['C3', 'C4', 'D3', 'D4', 'B3', 'B4', 'E3'], "Center block")
    test_configuration(['B2', 'B3', 'B4', 'C2', 'C4', 'D2', 'D3'], "Off-center block")

    # Edge configurations
    test_configuration(['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1'], "Top edge + 1")
    test_configuration(['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'A1'], "Middle column + 1")

    # Diagonal patterns
    test_configuration(['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'A6'], "Main diagonal + 1")
    test_configuration(['A6', 'B5', 'C4', 'D3', 'E2', 'F1', 'A1'], "Anti-diagonal + 1")

    # Scattered configurations
    test_configuration(['A1', 'B3', 'C5', 'D2', 'E4', 'F6', 'C1'], "Scattered 1")
    test_configuration(['A2', 'B4', 'C6', 'D1', 'E3', 'F5', 'A4'], "Scattered 2")
    test_configuration(['A3', 'B1', 'C4', 'D6', 'E2', 'F4', 'B5'], "Scattered 3")

    # Strategic blocking (block piece placement opportunities)
    test_configuration(['A1', 'A3', 'C1', 'C3', 'E1', 'E3', 'F2'], "Anti-L pattern")
    test_configuration(['B2', 'B4', 'D2', 'D4', 'F2', 'F4', 'A3'], "Checker-like")

    # Asymmetric configurations
    test_configuration(['A1', 'A2', 'B1', 'F5', 'F6', 'E6', 'C3'], "Clustered corners")
    test_configuration(['A1', 'F1', 'A6', 'F6', 'C3', 'C4', 'D3'], "Four corners + center")

if __name__ == "__main__":
    main()