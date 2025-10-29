import matrix
import exhaustive_search
import held_karp
import greedy_nearestneighbor
import time

if __name__ == '__main__':
    runs = 3
    test_cases = list(range(5, 31, 5))
    
    print("===============TRAVELING SALESPERSON PROBLEM===============")
    print("Legend:")
    print("ES = Exhaustive Search")
    print("HK = Bellman-Held-Karp algorithm")
    print("GNN = Greedy Nearest Neighbor algorithm")

    for case in test_cases:
        distance_matrix = matrix.gen_distance_matrix(case)
        print("\n==========================================================")
        print(f"                      Testing {case} Cities")
        print("==========================================================")


        # Lists to store per-run results
        es_times, es_costs = [], []
        hk_times, nn_times = [], []

        #EXHAUSTIVE SEARCH ALGORITHM
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
            result = held_karp.held_karp(distance_matrix)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            total_time_hk += elapsed_time
            hk_times.append(elapsed_time)

        # GREEDY NEAREST NEIGHBOR ALGORITHM
        total_time_nn = 0

        for run in range(runs):
            start_time = time.perf_counter()
            tour, cost = greedy_nearestneighbor.solve_nn_tsp(distance_matrix, start_city_index = 0)
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            total_time_nn += elapsed_time
            nn_times.append(elapsed_time)

        #TABULATED RESULTS
        def fmt(val):
            if val is None:
                return "N/A".ljust(8)
            return f"{val:.6f}".ljust(8)

        def fmt_cost(val):
            return str(val).ljust(8)

        # Header
        print("\n{:<6} {:<10} {:<15} {:<10} {:<10}".format(
            "Run", "ES (s)", "ES (best cost)", "HK (s)", "GNN (s)"
        ))
        print("-" * 58)

        # Rows per run
        for i in range(runs):
            print("{:<6} {:<10} {:<15} {:<10} {:<10}".format(
                f"{i+1}",
                fmt(es_times[i]),
                fmt_cost(es_costs[i]) if es_costs[i] is not None else "N/A".ljust(15),
                fmt(hk_times[i]),
                fmt(nn_times[i])
            ))

        # Compute averages
        avg_es = (sum(t for t in es_times if t is not None) / len([t for t in es_times if t is not None])
                  if any(t is not None for t in es_times) else None)
        avg_hk = sum(hk_times) / runs
        avg_nn = sum(nn_times) / runs
        best_cost = min(es_costs) if any(c is not None for c in es_costs) else "N/A"

        print("-" * 58)
        print("{:<6} {:<10} {:<15} {:<10} {:<10}".format(
            "Avg",
            fmt(avg_es),
            fmt_cost(best_cost),
            fmt(avg_hk),
            fmt(avg_nn)
        ))
        print("-" * 58 + "\n")