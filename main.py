import matrix
import held_karp
import time

if __name__ == '__main__':
    runs = 3
    test_cases = list(range(5, 31, 5))

    for i in test_cases:
        total = 0
        distance_matrix = matrix.gen_distance_matrix(i)

        # held karp
        for j in range(runs):
            start_time = time.perf_counter()
            result = held_karp.held_karp(distance_matrix)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            total += elapsed_time

            # print(result) may be removed
            print(f"{elapsed_time:.6f} seconds")
        print(f"\n{i} cities average run time with Held-Karp: {total / 3} seconds\n")

        # insert loops to run the 2 other algorithms here
        # since they need to use the same distance matrix for each test case
    

            

    
