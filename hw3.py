import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def init_graph(n):
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = matrix[j][i] = np.random.randint(0, 10)
    return matrix


def prim(matrix):
    n = matrix.shape[0]
    distances = np.ones(n) * np.inf
    parent = [-1] * n
    visited = [False] * n

    start_node = 0
    distances[start_node] = 0

    for _ in range(n):
        u = -1
        for i in range(n):
            if not visited[i] and (u == -1 or distances[i] < distances[u]):
                u = i
        visited[u] = True

        for v in range(n):
            if not visited[v] and matrix[u, v] > 0 and matrix[u, v] < distances[v]:
                distances[v] = matrix[u, v]
                parent[v] = u

    min_spanning_tree = np.zeros((n, n))
    for v in range(1, n):
        u = parent[v]
        min_spanning_tree[u, v] = min_spanning_tree[v, u] = matrix[u, v]

    return nx.from_numpy_array(min_spanning_tree)


def remove_max(graph, num_edges_to_remove):
    matrix = nx.to_numpy_array(graph)

    edges = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            weight = matrix[i, j]
            if weight > 0:
                edges.append((i, j, weight))

    edges.sort(key=lambda x: -x[2])

    for i in range(min(num_edges_to_remove, len(edges))):
        edge = edges[i]
        matrix[edge[0], edge[1]] = 0
        matrix[edge[1], edge[0]] = 0

    return nx.from_numpy_array(matrix)


def draw(graph):
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw(graph, pos, node_size=100)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=10, font_family="sans-serif", font_color="b")
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif")
    plt.show()


if __name__ == '__main__':
    n = 4

    # граф
    matrix = init_graph(n)
    G = nx.from_numpy_array(matrix)
    draw(G)

    # минимальное дерево
    G = prim(nx.to_numpy_array(G))
    draw(G)

    # кластеры
    G = remove_max(G, 3)
    draw(G)
