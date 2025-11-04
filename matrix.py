import random

def gen_distance_matrix(n):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            rand_val = random.randint(10, 150)
            matrix[i][j] = rand_val
            matrix[j][i] = rand_val
    return matrix