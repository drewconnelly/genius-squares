def create_matrix(false_cells):
    """Create a 6x6 matrix where all cells are True except for specified false_cells."""
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    cols = [1, 2, 3, 4, 5, 6]
    
    matrix = {row: {col: True for col in cols} for row in rows}
    
    for cell in false_cells:
        row = cell[0].upper()
        col = int(cell[1])
        if row in rows and col in cols:
            matrix[row][col] = False
    
    return matrix


def print_matrix(matrix, placement=None, piece_colors=None):
    """Print the matrix with optional piece placement visualization."""
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    cols = [1, 2, 3, 4, 5, 6]

    print("   ", end="")
    for col in cols:
        print(f" {col} ", end="")
    print()

    for row in rows:
        print(f" {row} ", end="")
        for col in cols:
            if not matrix[row][col]:
                print(" X ", end="")
            elif placement and (row, col) in placement:
                piece_char = placement[(row, col)]
                if piece_colors and piece_char in piece_colors:
                    color = piece_colors[piece_char]
                    reset = piece_colors.get('RESET', '\033[0m')
                    print(f" {color}{piece_char}{reset} ", end="")
                else:
                    print(f" {piece_char} ", end="")
            else:
                print(" . ", end="")
        print()


# Define pieces as relative coordinates from anchor point (0,0)
# Each piece can have multiple rotations
def get_rotations(piece):
    """Generate all unique rotations of a piece."""
    rotations = []
    current = piece
    
    for _ in range(4):
        # Normalize: shift so min row and col are 0
        min_r = min(r for r, c in current)
        min_c = min(c for r, c in current)
        normalized = tuple(sorted((r - min_r, c - min_c) for r, c in current))
        
        if normalized not in rotations:
            rotations.append(normalized)
        
        # Rotate 90 degrees clockwise: (r, c) -> (c, -r)
        current = [(c, -r) for r, c in current]
    
    return rotations


def get_all_orientations(piece):
    """Get all rotations and reflections of a piece."""
    orientations = []
    
    # Original and its rotations
    orientations.extend(get_rotations(piece))
    
    # Reflected (flip horizontally) and its rotations
    reflected = [(r, -c) for r, c in piece]
    orientations.extend(get_rotations(reflected))
    
    # Remove duplicates
    unique = []
    for ori in orientations:
        if ori not in unique:
            unique.append(ori)
    
    return unique

def get_valid_placements(piece_name, piece_orientations, matrix):
    """Get all valid placements for a piece on the board."""
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    row_to_idx = {r: i for i, r in enumerate(rows)}
    idx_to_row = {i: r for i, r in enumerate(rows)}
    cols = [1, 2, 3, 4, 5, 6]
    
    placements = []
    
    for orientation in piece_orientations:
        # Try each possible anchor position
        for anchor_row_idx in range(6):
            for anchor_col_idx in range(6):
                cells = []
                valid = True
                
                for dr, dc in orientation:
                    r_idx = anchor_row_idx + dr
                    c_idx = anchor_col_idx + dc
                    
                    # Check bounds
                    if not (0 <= r_idx < 6 and 0 <= c_idx < 6):
                        valid = False
                        break
                    
                    row = idx_to_row[r_idx]
                    col = cols[c_idx]
                    
                    # Check if cell is available (True in matrix)
                    if not matrix[row][col]:
                        valid = False
                        break
                    
                    cells.append((row, col))
                
                if valid:
                    placements.append(frozenset(cells))
    
    # Remove duplicate placements
    return list(set(placements))


def solve_puzzle(matrix, pieces, find_all=True):
    """
    Find all solutions to place all pieces on the board.
    Uses backtracking with pruning.
    """
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    cols = [1, 2, 3, 4, 5, 6]
    
    # Get available cells
    available = set()
    for row in rows:
        for col in cols:
            if matrix[row][col]:
                available.add((row, col))
    
    # Precompute all valid placements for each piece
    piece_placements = {}
    for name, shape in pieces.items():
        orientations = get_all_orientations(shape)
        placements = get_valid_placements(name, orientations, matrix)
        piece_placements[name] = placements
        print(f"Piece {name}: {len(placements)} valid placements")
    
    # Check if total piece cells equals available cells
    total_piece_cells = sum(len(shape) for shape in pieces.values())
    print(f"\nTotal piece cells: {total_piece_cells}")
    print(f"Available board cells: {len(available)}")
    
    if total_piece_cells != len(available):
        print("Warning: Piece cells don't match available cells!")
        if total_piece_cells > len(available):
            return []
    
    solutions = []
    piece_names = list(pieces.keys())
    
    def backtrack(piece_idx, used_cells, current_placement):
        if piece_idx == len(piece_names):
            # All pieces placed successfully
            solutions.append(current_placement.copy())
            return
        
        piece_name = piece_names[piece_idx]
        
        for placement in piece_placements[piece_name]:
            # Check if placement overlaps with used cells
            if placement & used_cells:
                continue
            
            # Place the piece
            new_used = used_cells | placement
            current_placement[piece_name] = placement
            
            backtrack(piece_idx + 1, new_used, current_placement)
            
            if solutions and not find_all:
                return
            
            del current_placement[piece_name]
    
    backtrack(0, frozenset(), {})
    
    return solutions


def print_solution(matrix, solution, pieces, piece_colors=None):
    """Print a solution with pieces shown on the board."""
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    cols = [1, 2, 3, 4, 5, 6]

    # Create placement map
    placement = {}
    for piece_name, cells in solution.items():
        for cell in cells:
            placement[cell] = piece_name  # Use piece name

    print_matrix(matrix, placement, piece_colors)
