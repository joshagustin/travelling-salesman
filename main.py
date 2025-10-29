import matrix
import held_karp
import greedy_nearestneighbor
import time

if __name__ == '__main__':
    runs = 3
    test_cases = list(range(5, 31, 5))
    
    for case in test_cases:
        distance_matrix = matrix.gen_distance_matrix(case)

        # insert EXHAUSTIVE SEARCH ALGORITHM here
        # use "total_time_es" for total time

        # DP HELD KARP ALGORITHM
        print(f"--- Testing n = {case} cities (Held-Karp) ---")
        total_time_hk = 0  # Use a unique variable for Held-Karp time

        for run in range(runs):
            start_time = time.perf_counter()
            result = held_karp.held_karp(distance_matrix)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            total_time_hk += elapsed_time

            print(f"{elapsed_time:.6f} seconds")
        
        print(f"\n{case} cities average run time with Held-Karp: {total_time_hk / runs:.6f} seconds\n")

        # GREEDY NEAREST NEIGHBOR ALGORITHM
        print(f"--- Testing n = {case} cities (Greedy Nearest Neighbor) ---")
        total_time_nn = 0

        for run in range(runs):
            start_time = time.perf_counter()
            tour, cost = greedy_nearestneighbor.solve_nn_tsp(distance_matrix, start_city_index = 0)
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            total_time_nn += elapsed_time

            print(f"{elapsed_time:.6f} seconds")

        print(f"\n{case} cities average run time with Greedy Nearest Neighbor: {total_time_nn / runs:.6f} seconds\n")
        print("--------------------------------------------------\n")
  

    

            

    
