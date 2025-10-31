import matrix
import exhaustive_search
import held_karp
import greedy_nearestneighbor
import time
import json
import numpy as np
from typing import List

def fmt(val):
    if val is None:
        return "N/A".ljust(8)
    return f"{val:.6f}".ljust(8)

def fmt_cost(val):
    return str(val).ljust(8)

def tabulate(es_times, es_costs, hk_times, hk_costs, nn_times, nn_costs):
    print("\n{:<6} {:<10} {:<15} {:<10} {:<15} {:<10} {:<15}".format(
        "Run", "ES (s)", "ES (best cost)", "HK (s)", "HK (best cost)", "GNN (s)", "GNN (best cost)"
    ))
    print("-" * 88)

    # Rows per run
    for i in range(runs):
        print("{:<6} {:<10} {:<15} {:<10} {:<15} {:<10} {:<15}".format(
            f"{i+1}",
            fmt(es_times[i]),
            fmt_cost(es_costs[i]) if es_costs[i] is not None else "N/A".ljust(15),
            fmt(hk_times[i]),
            fmt_cost(hk_costs[i]),
            fmt(nn_times[i]),
            fmt_cost(nn_costs[i])
        ))

    # Compute averages
    avg_es = sum(t for t in es_times if t is not None) / runs if any(t is not None for t in es_times) else None
    avg_hk = sum(t for t in hk_times if t is not None) / runs if any(t is not None for t in hk_times) else None
    avg_nn = sum(nn_times) / runs
    es_best_cost = min([c for c in es_costs if c is not None]) if any(c is not None for c in es_costs) else None
    hk_best_cost = min([c for c in hk_costs if c is not None]) if any(c is not None for c in hk_costs) else None
    nn_best_cost = min(nn_costs)

    print("-" * 88)
    print("{:<6} {:<10} {:<15} {:<10} {:<15} {:<10} {:<15}".format(
        "Avg",
        fmt(avg_es),
        fmt_cost(es_best_cost),
        fmt(avg_hk),
        fmt_cost(hk_best_cost),
        fmt(avg_nn),
        fmt_cost(nn_best_cost)
    ))
    print("-" * 88 + "\n")
    
    return avg_es, avg_hk, avg_nn, es_best_cost, hk_best_cost, nn_best_cost

def extrapolate_times(actual_times: List[float], actual_n: List[int], target_n: List[int], algorithm: str) -> List[float]:
    """
   extraploate based on known complexity trends
    """
    if not actual_times:
        return [None] * len(target_n)
    
    actual_n_arr = np.array(actual_n)
    actual_times_arr = np.array(actual_times)
    
    # Fit based on expected complexity
    if algorithm == "ES":
        # O(n!) complexity - fit to exponential growth
        log_factorial = np.array([sum(np.log(range(2, n+1))) for n in actual_n_arr])
        coeffs = np.polyfit(log_factorial, np.log(actual_times_arr), 1)
        extrapolated = []
        for n in target_n:
            if n <= max(actual_n_arr):
                # Use actual measurement
                idx = actual_n_arr.tolist().index(n)
                extrapolated.append(actual_times_arr[idx])
            else:
                # Extrapolate using factorial growth
                pred_log_time = coeffs[0] * sum(np.log(range(2, n+1))) + coeffs[1]
                extrapolated.append(np.exp(pred_log_time))
    
    elif algorithm == "HK":
        # O(n^2 * 2^n) complexity
        log_complexity = np.array([2*np.log(n) + n*np.log(2) for n in actual_n_arr])
        coeffs = np.polyfit(log_complexity, np.log(actual_times_arr), 1)
        extrapolated = []
        for n in target_n:
            if n <= max(actual_n_arr):
                idx = actual_n_arr.tolist().index(n)
                extrapolated.append(actual_times_arr[idx])
            else:
                pred_log_time = coeffs[0] * (2*np.log(n) + n*np.log(2)) + coeffs[1]
                extrapolated.append(np.exp(pred_log_time))
    
    else:  # NN - O(n^2) complexity
        log_complexity = np.array([2*np.log(n) for n in actual_n_arr])
        coeffs = np.polyfit(log_complexity, np.log(actual_times_arr), 1)
        extrapolated = []
        for n in target_n:
            if n <= max(actual_n_arr):
                idx = actual_n_arr.tolist().index(n)
                extrapolated.append(actual_times_arr[idx])
            else:
                pred_log_time = coeffs[0] * (2*np.log(n)) + coeffs[1]
                extrapolated.append(np.exp(pred_log_time))
    
    return extrapolated

if __name__ == '__main__':
    runs = 3
    test_cases = list(range(3, 31, 3))
    
    # Determine maximum feasible n for each algorithm
    max_feasible_es = 12  # set for the mean time
    max_feasible_hk = 20  # set for the mean time to see generated graphs
    
    # Lists to store results for plotting
    es_avg_times = []
    hk_avg_times = []
    nn_avg_times = []
    es_best_costs = []
    hk_best_costs = []
    nn_best_costs = []
    all_test_cases = []
    
    text = "TRAVELING SALESPERSON PROBLEM"
    print(text.center(88, '='))
    print("Legend:")
    print("ES = Exhaustive Search")
    print("HK = Bellman-Held-Karp algorithm")
    print("GNN = Greedy Nearest Neighbor algorithm")
    print(f"\nMaximum feasible sizes:")
    print(f"ES: {max_feasible_es} cities")
    print(f"HK: {max_feasible_hk} cities")
    print(f"GNN: All test cases")

    for case in test_cases:
        distance_matrix = matrix.gen_distance_matrix(case)
        print("\n")
        print("="*88)
        text = f"Testing {case} Cities"
        print(text.center(88))
        print("="*88)

        # Lists to store per-run results
        es_times, es_costs = [], []
        hk_times, hk_costs = [], []
        nn_times, nn_costs = [], []

        # EXHAUSTIVE SEARCH ALGORITHM
        if case <= max_feasible_es:
            for run in range(runs):
                start_time = time.perf_counter()
                tour, cost = exhaustive_search.solve_tsp_exhaustive(distance_matrix)
                end_time = time.perf_counter()
                
                elapsed_time = end_time - start_time
                es_times.append(elapsed_time)
                es_costs.append(cost)
        else:
            es_times = [None] * runs
            es_costs = [None] * runs

        # DP HELD KARP ALGORITHM
        if case <= max_feasible_hk:
            for run in range(runs):
                start_time = time.perf_counter()
                cost, tour = held_karp.held_karp(distance_matrix)
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time
                hk_times.append(elapsed_time)
                hk_costs.append(cost)
        else:
            hk_times = [None] * runs
            hk_costs = [None] * runs

        # GREEDY NEAREST NEIGHBOR ALGORITHM 
        for run in range(runs):
            start_time = time.perf_counter()
            tour, cost = greedy_nearestneighbor.solve_nn_tsp(distance_matrix, start_city_index=0)
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            nn_times.append(elapsed_time)
            nn_costs.append(cost)

        # Get average times and store for plotting
        avg_es, avg_hk, avg_nn, best_es, best_hk, best_nn = tabulate(
            es_times, es_costs, hk_times, hk_costs, nn_times, nn_costs
        )
        
        es_avg_times.append(avg_es)
        hk_avg_times.append(avg_hk)
        nn_avg_times.append(avg_nn)
        es_best_costs.append(best_es if best_es != "N/A" else None)
        hk_best_costs.append(best_hk if best_hk != "N/A" else None)
        nn_best_costs.append(best_nn)
        all_test_cases.append(case)
    
    # Extrapolate results for larger n values
    print("\n" + "="*88)
    print("EXTRAPOLATING RESULTS FOR LARGER PROBLEM SIZES")
    print("="*88)
    
    # Get actual measured data for extrapolation
    es_measured_n = [n for i, n in enumerate(all_test_cases) if es_avg_times[i] is not None]
    es_measured_times = [t for t in es_avg_times if t is not None]
    
    hk_measured_n = [n for i, n in enumerate(all_test_cases) if hk_avg_times[i] is not None]
    hk_measured_times = [t for t in hk_avg_times if t is not None]
    
    nn_measured_n = [n for i, n in enumerate(all_test_cases) if nn_avg_times[i] is not None]
    nn_measured_times = [t for t in nn_avg_times if t is not None]
    
    # Extrapolate
    es_extrapolated = extrapolate_times(es_measured_times, es_measured_n, all_test_cases, "ES")
    hk_extrapolated = extrapolate_times(hk_measured_times, hk_measured_n, all_test_cases, "HK")
    nn_extrapolated = extrapolate_times(nn_measured_times, nn_measured_n, all_test_cases, "NN")
    
    # Save results to a file for visualization
    results = {
        'test_cases': all_test_cases,
        'es_avg_times': es_avg_times,
        'hk_avg_times': hk_avg_times,
        'nn_avg_times': nn_avg_times,
        'es_best_costs': es_best_costs,
        'hk_best_costs': hk_best_costs,
        'nn_best_costs': nn_best_costs,
        'es_extrapolated': es_extrapolated,
        'hk_extrapolated': hk_extrapolated,
        'nn_extrapolated': nn_extrapolated,
        'max_feasible_es': max_feasible_es,
        'max_feasible_hk': max_feasible_hk
    }
    
    with open('tsp_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to 'tsp_results.json'")
    print(f"Maximum successfully terminated:")
    print(f"  Exhaustive Search: {max_feasible_es} cities")
    print(f"  Held-Karp: {max_feasible_hk} cities")
    print(f"  Greedy Nearest Neighbor: {max(all_test_cases)} cities")
    print("\nRun 'graphs_results.py' to generate performance plots.")