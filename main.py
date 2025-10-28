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
        for run in range(runs):
            start_time = time.perf_counter()
            result = held_karp.held_karp(distance_matrix)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            total_time += elapsed_time

            # print(result) may be removed
            print(f"{elapsed_time:.6f} seconds")
        print(f"\n{case} cities average run time with Held-Karp: {total_time / 3} seconds\n")

        # insert loops to run the 2 other algorithms here
        # since they need to use the same distance matrix for each test case
    

            

    
