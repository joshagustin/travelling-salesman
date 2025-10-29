import sys

def solve_nn_tsp(dist_matrix, start_city_index=0):
    """
    Solves the TSP using the Greedy Nearest Neighbor heuristic.

    Args:
        dist_matrix (numpy.ndarray): The n x n distance matrix.
        start_city_index (int): The index of the starting city.

    Returns:
        tuple: A tuple containing:
            - list: The tour (path) as a list of city indices.
            - int: The total cost of the tour.
    """
    n = len(dist_matrix)

    # Keeps track of visited cities
    visited = [False] * n

    # Stores the tour
    tour = []
    total_cost = 0

    # Starts at the given city
    current_city = start_city_index
    tour.append(current_city)
    visited[current_city] = True

    # === Main Loop: Visit all n-1 remaining cities ===
    for _ in range(n - 1):
        nearest_city = -1
        min_dist = sys.maxsize

        # Find the nearest *unvisited* city
        for city in range(n):
            # Check if the city is unvisited AND it's a closer path
            if not visited[city] and dist_matrix[current_city][city] < min_dist:
                min_dist = dist_matrix[current_city][city]
                nearest_city = city

        # Travel to the nearest city
        if nearest_city != -1:
            total_cost += min_dist
            current_city = nearest_city
            tour.append(current_city)
            visited[current_city] = True

    # === Complete the tour: Go back to the start ===
    # Adds cost from the last city to the starting city
    total_cost += dist_matrix[current_city][start_city_index]
    tour.append(start_city_index)

    return tour, total_cost