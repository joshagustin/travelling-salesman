import matrix
import exhaustive_search
import held_karp
import greedy_nearestneighbor
import time

def fmt(val):
    if val is None:
        return "N/A".ljust(8)
    return f"{val:.6f}".ljust(8)

def fmt_cost(val):
    return str(val).ljust(8)

def tabulate(es_times, es_costs, hk_times, hk_costs, nn_times, nn_costs):
    # Header
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
    avg_es = (sum(t for t in es_times if t is not None) / len([t for t in es_times if t is not None])
                if any(t is not None for t in es_times) else None)
    avg_hk = sum(hk_times) / runs
    avg_nn = sum(nn_times) / runs
    es_best_cost = min(es_costs) if any(c is not None for c in es_costs) else "N/A"
    hk_best_cost = min(hk_costs)
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

if __name__ == '__main__':
    runs = 3
    test_cases = list(range(5, 31, 5))
    
    text = "TRAVELING SALESPERSON PROBLEM"
    print(text.center(88, '='))
    print("Legend:")
    print("ES = Exhaustive Search")
    print("HK = Bellman-Held-Karp algorithm")
    print("GNN = Greedy Nearest Neighbor algorithm")

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
        if case <= 15:
            total_time_es = 0

            for run in range(runs):
                start_time = time.perf_counter()
                tour, cost = exhaustive_search.solve_tsp_exhaustive(distance_matrix)
                end_time = time.perf_counter()
                
                elapsed_time = end_time - start_time
                total_time_es += elapsed_time

                es_times.append(elapsed_time)
                es_costs.append(cost)
        else:
            total_time_es = None
            es_times = [None] * runs
            es_costs = [None] * runs

        # DP HELD KARP ALGORITHM
        total_time_hk = 0  # Use a unique variable for Held-Karp time

        for run in range(runs):
            start_time = time.perf_counter()
            cost, tour = held_karp.held_karp(distance_matrix)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            total_time_hk += elapsed_time

            hk_times.append(elapsed_time)
            hk_costs.append(cost)

        # GREEDY NEAREST NEIGHBOR ALGORITHM
        total_time_nn = 0

        for run in range(runs):
            start_time = time.perf_counter()
            tour, cost = greedy_nearestneighbor.solve_nn_tsp(distance_matrix, start_city_index = 0)
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            total_time_nn += elapsed_time

            nn_times.append(elapsed_time)
            nn_costs.append(cost)

        tabulate(es_times, es_costs, hk_times, hk_costs, nn_times, nn_costs)