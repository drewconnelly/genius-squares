#!/usr/bin/env python3
"""
Analyze different false_cells configurations to find the one with the least solutions.
"""

from geniusSquare import create_matrix, solve_puzzle
from itertools import combinations
import time

# Import pieces from play.py
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

def generate_all_cells():
    """Generate all possible cell positions on a 6x6 board."""
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    cols = [1, 2, 3, 4, 5, 6]
    return [f"{row}{col}" for row in rows for col in cols]

def analyze_configuration(false_cells, max_solutions=1000):
    """Analyze a single configuration and return number of solutions."""
    try:
        matrix = create_matrix(false_cells)

        # Calculate required pieces for available cells
        available_cells = 36 - len(false_cells)

        # Check if we can make exactly the right number of cells with our pieces
        total_piece_cells = sum(len(shape) for shape in PIECES.values())

        if available_cells != total_piece_cells:
            return None, f"Cell mismatch: {available_cells} available, {total_piece_cells} piece cells"

        # Find solutions (limit to avoid very long computations)
        start_time = time.time()
        solutions = solve_puzzle(matrix, PIECES, find_all=True)
        end_time = time.time()

        # If it takes too long, we might want to stop early
        if end_time - start_time > 60:  # 60 seconds timeout
            return None, "Timeout"

        return len(solutions), f"Time: {end_time - start_time:.2f}s"

    except Exception as e:
        return None, f"Error: {str(e)}"

def find_optimal_configurations(num_false_cells=7, sample_size=100):
    """
    Find configurations with the least number of solutions.

    Args:
        num_false_cells: Number of cells to block (default 7 to match current setup)
        sample_size: Number of random configurations to test (None for all)
    """
    all_cells = generate_all_cells()

    print(f"Analyzing configurations with {num_false_cells} blocked cells...")
    print(f"Total possible combinations: {len(list(combinations(all_cells, num_false_cells)))}")

    results = []
    tested = 0

    # Generate all possible combinations
    all_combinations = list(combinations(all_cells, num_false_cells))

    # If sample_size is specified and less than total, sample randomly
    if sample_size and sample_size < len(all_combinations):
        import random
        random.seed(42)  # For reproducible results
        test_combinations = random.sample(all_combinations, sample_size)
        print(f"Testing random sample of {sample_size} configurations...")
    else:
        test_combinations = all_combinations
        print(f"Testing all {len(all_combinations)} configurations...")

    for i, false_cells in enumerate(test_combinations):
        if i % 50 == 0:
            print(f"Progress: {i}/{len(test_combinations)} ({i/len(test_combinations)*100:.1f}%)")

        solution_count, info = analyze_configuration(list(false_cells))

        if solution_count is not None:
            results.append((solution_count, list(false_cells), info))
            tested += 1

        # Print interesting results as we find them
        if solution_count is not None and solution_count <= 5:
            print(f"  Found low-solution config: {solution_count} solutions - {false_cells}")

    print(f"\nTested {tested} valid configurations")

    # Sort by number of solutions (ascending)
    results.sort(key=lambda x: x[0])

    return results

def main():
    """Main analysis function."""
    print("=== False Cells Configuration Analysis ===\n")

    # Test current configuration first

    # add some constraints to the possible values for current_config
    # first cell is either F1 or A6

    current_config = ['A1', 'A3', 'A5', 'C5', 'D3', 'D5', 'F1']
    print("Testing current configuration:", current_config)
    solution_count, info = analyze_configuration(current_config)
    print(f"Current config has {solution_count} solutions ({info})\n")

    # Find optimal configurations
    # Start with a smaller sample to see the range
    results = find_optimal_configurations(num_false_cells=7, sample_size=200)

    if results:
        print(f"\n=== Top 10 Configurations with Fewest Solutions ===")
        for i, (count, cells, info) in enumerate(results[:10]):
            print(f"{i+1:2d}. {count:3d} solutions - {cells} ({info})")

        print(f"\n=== Bottom 5 Configurations with Most Solutions ===")
        for i, (count, cells, info) in enumerate(results[-5:]):
            rank = len(results) - 4 + i
            print(f"{rank:2d}. {count:3d} solutions - {cells} ({info})")

        # Statistics
        solution_counts = [r[0] for r in results]
        print(f"\n=== Statistics ===")
        print(f"Minimum solutions: {min(solution_counts)}")
        print(f"Maximum solutions: {max(solution_counts)}")
        print(f"Average solutions: {sum(solution_counts)/len(solution_counts):.1f}")
        print(f"Configurations tested: {len(results)}")

if __name__ == "__main__":
    main()