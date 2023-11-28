import random
import sys

import matplotlib.pyplot as plt
import numpy as np


# генерация точек
def get_points(n = 100):
    points = []
    for i in range(n):
        points.append([random.randint(0,100),
                       random.randint(0,100)])
    return points

# визуализация точек разделенных на кластеры и их центроидов
def visualize_points(points ,centroids, clusters=None):
    colors = ['lime', 'g', 'b', 'c', 'm', 'y', 'k', 'gold', 'magenta', 'teal', 'cyan']

    if clusters:
        point_colors = [colors[c] for c in clusters]
        plt.scatter(*zip(*points), c=point_colors)
    else:
        plt.scatter(*zip(*points), c='black')

    plt.scatter(*zip(*centroids), color='r')
    plt.show()

# расстояние между двумя точками
def dist(pointA, pointB):
    return np.sqrt((pointA[0]-pointB[0])**2+
                   (pointA[1]-pointB[1])**2)

# возвращает центр оркужности, лежащий на среднем значении x,y всех точек,
# и радиус этой окружности, равный расстоянию от центра окружности до самой удалённой точки.
def set_boundary(points):
    center = [0,0]
    for point in points:
        center[0] += point[0]
        center[1] += point[1]
    center[0] /= len(points)
    center[1] /= len(points)
    R=0
    for point in points:
        d = dist(center, point)
        if(d > R):
            R = d
    return center,  R

# возвращает массив центроидов, расположенных равномерно по окружности.
def set_centroids(points, k=4):
    center, R = set_boundary(points)
    centroids = []
    for i in range(k):
        centroids.append(
            [R*np.cos(2*np.pi*i/k)+center[0],
             R*np.sin(2*np.pi*i/k)+center[1]])
    return centroids

# возвращает точки для каждого кластера
def nearby_point(points, centroids):
    clusters = []
    for point in points:
        r, index = 10000000, -1
        for i in range(len(centroids)):
            d = dist(point, centroids[i])
            if(r>d):
                r = d
                index = i
        clusters.append(index)
    return clusters

# возвращает новые координаты центроидов для заданных кластеров
def move_centroids(points, clusters):
    count_of_clusters = len(set(clusters))
    sum_of_coordinates = [[0, 0, 0] for _ in range(count_of_clusters)]

    for point, cluster in zip(points, clusters):
        sum_of_coordinates[cluster][0] += point[0]
        sum_of_coordinates[cluster][1] += point[1]
        sum_of_coordinates[cluster][2] += 1

    new_centroids = []

    for sum_x, sum_y, count in sum_of_coordinates:
        if count > 0:
            new_x = round(sum_x / count, 1)
            new_y = round(sum_y / count, 1)
            new_centroids.append([new_x, new_y])

    return new_centroids

def kmeans(points, k):
    # Инициализация центроидов случайным образом
    centroids = set_centroids(points, k)
    clusters = []
    # Ищет лучшее расположение цетроидов для кластеров
    while True:
            new_clusters = nearby_point(points, centroids)
            if np.array_equiv(clusters, new_clusters):
                break
            clusters = new_clusters
            new_centroids = move_centroids(points, clusters)
            centroids = new_centroids

    return clusters, centroids

def kmeans_with_visualization(points, k):
    # Инициализация центроидов случайным образом
    centroids = set_centroids(points, k)
    clusters = []

    while True:
            new_clusters = nearby_point(points, centroids)
            visualize_points(points ,centroids, clusters)
            if np.array_equiv(clusters, new_clusters):
                break
            clusters = new_clusters
            new_centroids = move_centroids(points, clusters)
            centroids = new_centroids

    return clusters, centroids

# сумма квадратов расстояний для заданных точек и центроидов
def get_sum_of_square_distances(points, centroids, clusters):
    distances = [0] * len(centroids)
    total_distance = 0

    for point_index in range(len(points)):
        distances[clusters[point_index]] = dist(
            points[point_index],
            centroids[clusters[point_index]]
        )
    for index in range(len(distances)):
        total_distance += distances[index]
    return total_distance

def elbow_method(points):
    sums_of_square_distances = []
    for k in range(1, 11):
        clusters, centroids = kmeans(points, k)
        sum_of_square_distances = get_sum_of_square_distances(points, centroids, clusters)

        sums_of_square_distances.append(sum_of_square_distances)

    # Вычисление D(k)
    fall_rates_measures = [0] * 11
    for k_index, sum_of_squares_of_distances in enumerate(sums_of_square_distances[1:-1], start=1):
        fall_rates_measures[k_index] = abs(
            sum_of_squares_of_distances - sums_of_square_distances[k_index + 1]) / abs(
            sums_of_square_distances[k_index - 1] - sum_of_squares_of_distances)

    # Поиск оптимального k
    optimal_k = -1
    min_value = sys.maxsize
    for k_index in range(len(fall_rates_measures)):
        current_distance = fall_rates_measures[k_index]
        if (current_distance < min_value) and (current_distance != 0):
            min_value = current_distance
            optimal_k = k_index

    return optimal_k


if __name__ == '__main__':
    points = get_points()
    optimal_k = elbow_method(points)
    print('Optimal clusters amount: ', optimal_k)
    kmeans_with_visualization(points, optimal_k)