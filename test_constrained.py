#!/usr/bin/env python3
"""
Quick test of constrained combinations with parallel processing.
"""

from itertools import product
from geniusSquare import create_matrix, solve_puzzle
from multiprocessing import Pool, cpu_count
import time

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

def generate_constrained_combinations():
    """Generate all possible combinations based on position constraints."""
    position_constraints = {
        0: ['A6', 'F1'],
        1: ['E3', 'C3', 'C4', 'D3', 'B4', 'D4'],
        2: ['A1', 'C1', 'D1', 'D2', 'E2', 'F3'],
        3: ['A4', 'B5', 'C5', 'C6', 'D6', 'F6'],
        4: ['A5', 'B6', 'E1', 'F2'],
        5: ['D5', 'E4', 'E5', 'E6', 'F4', 'F5'],
        6: ['A2', 'A3', 'B1', 'B2', 'B3', 'C2']
    }

    # Generate all combinations of the constraints
    all_combinations = []
    for combo in product(*[position_constraints[i] for i in range(7)]):
        # Check for duplicates (same cell chosen for multiple positions)
        if len(set(combo)) == 7:  # All 7 positions have unique cells
            all_combinations.append(list(combo))

    return all_combinations

def test_config(false_cells):
    """Test a configuration and return the number of solutions."""
    try:
        matrix = create_matrix(false_cells)
        solutions = solve_puzzle(matrix, PIECES, find_all=True)
        return (false_cells, len(solutions))
    except Exception as e:
        return (false_cells, None)

def test_configs_parallel(combinations, num_processes=None, progress_interval=1000):
    """Test multiple configurations in parallel with progress updates."""
    if num_processes is None:
        num_processes = cpu_count()

    print(f"Using {num_processes} processes for parallel computation...")
    print(f"Testing {len(combinations)} total combinations...")

    start_time = time.time()
    all_results = []
    best_configs = []  # Track configurations with fewest solutions

    # Process in chunks for progress updates
    chunk_size = progress_interval
    total_chunks = (len(combinations) + chunk_size - 1) // chunk_size

    for chunk_idx in range(total_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, len(combinations))
        chunk = combinations[start_idx:end_idx]

        chunk_start_time = time.time()

        with Pool(num_processes) as pool:
            chunk_results = pool.map(test_config, chunk)

        chunk_end_time = time.time()
        all_results.extend(chunk_results)

        # Update progress and show current best results
        completed = end_idx
        progress_pct = (completed / len(combinations)) * 100
        elapsed_total = chunk_end_time - start_time
        chunk_time = chunk_end_time - chunk_start_time

        # Find valid results and current best
        valid_chunk_results = [(config, count) for config, count in chunk_results if count is not None]
        if valid_chunk_results:
            valid_chunk_results.sort(key=lambda x: x[1])
            best_configs.extend(valid_chunk_results)
            best_configs.sort(key=lambda x: x[1])
            best_configs = best_configs[:10]  # Keep only top 10

        print(f"\n--- Progress Update ---")
        print(f"Completed: {completed:,}/{len(combinations):,} ({progress_pct:.1f}%)")
        print(f"Chunk time: {chunk_time:.2f}s | Total time: {elapsed_total:.2f}s")
        print(f"Valid results in chunk: {len(valid_chunk_results)}/{len(chunk)}")

        if best_configs:
            print(f"Current best configuration: {best_configs[0][1]} solutions - {best_configs[0][0]}")
            if len(best_configs) >= 3:
                print(f"Top 3 solution counts: {[x[1] for x in best_configs[:3]]}")

    end_time = time.time()
    print(f"\nParallel processing completed in {end_time - start_time:.2f} seconds")

    return all_results

if __name__ == "__main__":
    # Count total combinations
    combinations = generate_constrained_combinations()
    print(f"Total constrained combinations: {len(combinations)}")

    # Calculate theoretical maximum (without duplicate checking)
    theoretical = 2 * 6 * 6 * 6 * 4 * 6 * 6
    print(f"Theoretical maximum (with duplicates): {theoretical}")

    # Test ALL combinations in parallel
    print(f"\nTesting ALL {len(combinations)} combinations in parallel:")

    results = test_configs_parallel(combinations)

    # Sort by solution count (ascending)
    valid_results = [(config, count) for config, count in results if count is not None]
    valid_results.sort(key=lambda x: x[1])

    print(f"\n=== Top 10 configurations with fewest solutions ===")
    for i, (config, solutions) in enumerate(valid_results[:10]):
        print(f"{i+1:2d}. {solutions:3d} solutions - {config}")

    print(f"\n=== Summary ===")
    print(f"Total tested: {len(results)}")
    print(f"Valid results: {len(valid_results)}")
    print(f"Errors: {len(results) - len(valid_results)}")
    if valid_results:
        solution_counts = [count for _, count in valid_results]
        print(f"Min solutions: {min(solution_counts)}")
        print(f"Max solutions: {max(solution_counts)}")
        print(f"Avg solutions: {sum(solution_counts)/len(solution_counts):.1f}")

    # Test current configuration if it matches constraints
    current = ['A1', 'A3', 'A5', 'C5', 'D3', 'D5', 'F1']
    print(f"\nCurrent config: {current}")

    # Check if current matches any constrained combination
    if current in combinations:
        print("Current config matches constraints!")
        solutions = test_config(current)
        print(f"Current config solutions: {solutions}")
    else:
        print("Current config does NOT match constraints")