# Example usage
from geniusSquare import create_matrix, print_matrix, print_solution, solve_puzzle

# Define your 9 tetris-style pieces here
# Each piece is a list of (row_offset, col_offset) from anchor
PIECES = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],          # I-piece (4 cells)
    'A': [(0, 0), (0, 1), (0, 2)],                  # I-piece (3 cells)
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],          # O-piece (4 cells, square)
    'T': [(0, 0), (0, 1), (0, 2), (1, 1)],          # T-piece (4 cells)
    'S': [(0, 1), (0, 2), (1, 0), (1, 1)],          # S-piece (4 cells)
    '1': [(0, 0)],                                  # one-piece (1 cell)
    '2': [(0, 0), (0, 1)],                          # two-piece (2 cells)
    'L': [(0, 0), (0, 1), (1, 0)],                  # L-piece (3 cells)
    'J': [(0, 0), (0, 1), (0, 2), (1, 0)],                  # J-piece (4 cells)
}

# ANSI color codes for pieces
PIECE_COLORS = {
    'I': '\033[90m',    # Grey
    'A': '\033[38;5;208m',  # Orange
    'O': '\033[92m',    # Green
    'T': '\033[93m',    # Yellow
    'S': '\033[91m',    # Red
    '1': '\033[94m',    # Blue
    '2': '\033[38;5;94m',   # Brown
    'L': '\033[95m',    # Magenta
    'J': '\033[96m',    # Cyan
}
RESET_COLOR = '\033[0m'

# Main execution
if __name__ == "__main__":
    # Define which cells are blocked (False)
    false_cells = ['A6', 'E3', 'A1', 'A4', 'F2', 'F4', 'B2']
    
    # Create the board
    matrix = create_matrix(false_cells)
    
    # Create color mapping for display
    colors_with_reset = PIECE_COLORS.copy()
    colors_with_reset['RESET'] = RESET_COLOR

    print("Board (X = blocked, . = available):")
    print_matrix(matrix)
    print()
    
    # You can customize which pieces to use
    # Make sure total cells match available cells (36 - len(false_cells))
    available_cells = 36 - len(false_cells)  # 29 cells
    
    print(f"Available cells: {available_cells}")
    print(f"You need pieces totaling exactly {available_cells} cells.\n")
    
    # Example: Select pieces that sum to available cells
    # Adjust this based on your actual pieces
    selected_pieces = {
        'I': PIECES['I'],  # 4
        'A': PIECES['A'],  # 4
        'O': PIECES['O'],  # 4
        'T': PIECES['T'],  # 4
        'S': PIECES['S'],  # 4
        '1': PIECES['1'],  # 4
        '2': PIECES['2'],  # 4
        'L': PIECES['L'],  # 5
        'J': PIECES['J'],  # 5
    }  # Total: 29 cells
    
    print("Finding solutions...\n")
    solutions = solve_puzzle(matrix, selected_pieces, find_all=True)
    
    print(f"\nFound {len(solutions)} solution(s)")
    
    # Print first few solutions
    for i, sol in enumerate(solutions[:5]):
        print(f"\n--- Solution {i + 1} ---")
        print_solution(matrix, sol, selected_pieces, colors_with_reset)