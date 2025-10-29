import matrix
import held_karp
import time

if __name__ == '__main__':
    runs = 3
    test_cases = list(range(5, 31, 5))

    for case in test_cases:
        total_time = 0
        distance_matrix = matrix.gen_distance_matrix(case)

        # held karp
        print(f"--- Testing n = {case} cities (Held-Karp) ---")
        
        for run in range(runs):
            start_time = time.perf_counter()
            result = held_karp.held_karp(distance_matrix)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            total_time += elapsed_time

            # print(result) may be removed
            print(f"{elapsed_time:.6f} seconds")
        print(f"\n{case} cities average run time with Held-Karp: {total_time / 3} seconds\n")

        # greedy nearest neighbor
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

        # insert loops to run the other algorithms here
        # since they need to use the same distance matrix for each test case
    

            

    
