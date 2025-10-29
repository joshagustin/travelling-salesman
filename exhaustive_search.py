import itertools

def solve_tsp_exhaustive(distance_matrix):
    """
    Solves the Traveling Salesperson Problem (TSP) using exhaustive search.
    The decrease-by-one method is utilized.

    Parameters:
        distance_matrix (list[list[int]]): Symmetric matrix of distances.

    Returns:
        best_tour (list[int]): The optimal tour (0-indexed, starting/ending at city 0).
        best_cost (float): The minimum total tour cost.
    """
    n = len(distance_matrix)
    cities = list(range(1, n))  # exclude start city (0)
    
    best_cost = float("inf")
    best_tour = []

    # Iterate over all permutations of remaining cities
    for perm in itertools.permutations(cities):
        tour = [0] + list(perm) + [0]  # start and end at city 0
        cost = 0
        # compute total cost for this tour
        for i in range(len(tour) - 1):
            cost += distance_matrix[tour[i]][tour[i + 1]]
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost