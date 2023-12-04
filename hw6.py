import random
import numpy as np

def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][route[0]]  # Return to the starting city
    return total_distance

def generate_random_route(num_cities, starting_city):
    route = list(range(num_cities))
    route.remove(starting_city)
    random.shuffle(route)
    route = [starting_city] + route
    return route

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]]
    child = child + [parent1[0]]  # Ensure the route ends in the starting city
    return child

def mutate(route):
    mutated_route = route.copy()
    index1, index2 = random.sample(range(1, len(route) - 1), 2)  # Avoid mutating the starting and ending city
    mutated_route[index1], mutated_route[index2] = mutated_route[index2], mutated_route[index1]
    return mutated_route

def genetic_algorithm(num_cities, starting_city, population_size, generations):
    distance_matrix = np.random.randint(1, 100, size=(num_cities, num_cities))
    np.fill_diagonal(distance_matrix, 0)
    print("Distances between cities:")
    for i in range(num_cities):
        for j in range(num_cities):
            print(distance_matrix[i][j], end="\t")
        print()
    population = [generate_random_route(num_cities, starting_city) for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = [1 / calculate_total_distance(route, distance_matrix) for route in population]
        parents = random.choices(population, weights=fitness_scores, k=population_size)
        next_generation = []

        for i in range(0, population_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            child1 = mutate(child1)
            child2 = mutate(child2)
            next_generation.extend([child1, child2])

        population = next_generation

    best_route = max(population, key=lambda route: 1 / calculate_total_distance(route, distance_matrix))

    return best_route, calculate_total_distance(best_route, distance_matrix)

if __name__ == "__main__":
    num_cities = 6
    STARTING_CITY = 0  # Set the starting city here
    population_size = 100
    generations = 1000

    best_route, best_distance = genetic_algorithm(num_cities, STARTING_CITY, population_size, generations)

    print("Best Route:", best_route)
    print("Total Distance:", best_distance)
