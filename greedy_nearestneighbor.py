import sys

def solve_nn_tsp(dist_matrix, start_city_index=0):
    """
    Implementation of a Greedy algorithm to solve the Traveling
    Salesman Problem using a Nearest Neighbor heuristic.

    Parameters:
        dist_matrix: distance matrix
        start_city_index: index of starting city

    Returns:
        tuple: (path, total_cost)
    """
    n = len(dist_matrix)

    # tracks visited cities
    visited = [False] * n

    # stores path
    path = []
    total_cost = 0

    # atarts at given city
    current_city = start_city_index
    path.append(current_city)
    visited[current_city] = True

    # MAIN LOOP: visit all n-1 remaining cities
    for _ in range(n - 1):
        nearest_city = -1
        min_dist = sys.maxsize

        # find the nearest *unvisited* city
        for city in range(n):
            # Check if the city is unvisited AND it's a closer path
            if not visited[city] and dist_matrix[current_city][city] < min_dist:
                min_dist = dist_matrix[current_city][city]
                nearest_city = city

        # travel to the nearest city
        if nearest_city != -1:
            total_cost += min_dist
            current_city = nearest_city
            path.append(current_city)
            visited[current_city] = True

    # adds cost from last city to starting city
    total_cost += dist_matrix[current_city][start_city_index]
    path.append(start_city_index)

    return path, total_cost