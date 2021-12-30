import random
import networkx as nx


class City:
    def __init__(self, identifiant: int, parent=None):
        self.parent = parent
        self.identifiant = identifiant
        self.g = 0
        self.h = 0
        self.f = 0
        self.list = []


def prims_algorithm(graph):
    adjacency_matrix = [[0 for _ in range(graph.number_of_nodes())] for _ in range(graph.number_of_nodes())]
    mst_matrix = [[0 for _ in range(graph.number_of_nodes())] for _ in range(graph.number_of_nodes())]

    for i in range(0, graph.number_of_nodes()):
        for j in range(0 + i, graph.number_of_nodes()):
            if i != j:
                adjacency_matrix[i][j] = graph[i][j]['weight']
                adjacency_matrix[j][i] = adjacency_matrix[i][j]

    infini = float('inf')
    selected_vertices = [False for _ in range(graph.number_of_nodes())]

    while False in selected_vertices:
        minimum = infini
        start = 0
        end = 0
        for i in range(0, graph.number_of_nodes()):
            if selected_vertices[i]:
                for j in range(0 + i, graph.number_of_nodes()):
                    if not selected_vertices[j] and adjacency_matrix[i][j] > 0:
                        if adjacency_matrix[i][j] < minimum:
                            minimum = adjacency_matrix[i][j]
                            start, end = i, j
        selected_vertices[end] = True
        mst_matrix[start][end] = minimum

        if minimum == infini:
            mst_matrix[start][end] = 0

        mst_matrix[end][start] = mst_matrix[start][end]
    return sum(sum(mst_matrix, []))


def A_star(graph):
    initial_city = City(random.randint(0, len(graph.nodes())-1), parent=None)
    initial_city.g = initial_city.h = initial_city.f = 0

    frontier = []
    max_frontier_length = len(frontier)
    cities_already_explored = []
    id_of_visited_cities = set()
    cities_to_visit = [initial_city.identifiant]
    for n in graph.nodes():
        cities_to_visit.append(n)

    initial_city.list = cities_to_visit
    frontier.append(initial_city)

    while len(frontier) > 0:
        current_city = frontier[0]
        current_index = 0
        for index, item in enumerate(frontier):
            if item.f < current_city.f:
                current_city = item
                current_index = index

        frontier.pop(current_index)
        cities_already_explored.append(current_city)
        id_of_visited_cities.add(current_city.identifiant)
        print("flag", current_city.identifiant)
        #current_city.list.remove(current_city.identifiant)
        cities_to_visit.remove(current_city.identifiant)

        # Found the goal
        if current_city.identifiant == initial_city.identifiant and len(cities_to_visit) == 0:
            path = []
            current = current_city
            while current is not None:
                path.append(current.identifiant)
                current = current.parent
            return path

        # Generate children
        children = []
        for id in cities_to_visit:
            if id != current_city.identifiant:
                city = City(identifiant=id, parent=current_city)
                children.append(city)

        # Loop through children
        for child in children:
            # Create the f, g, and h values
            print("TEST: ", current_city.identifiant, child.identifiant)
            child.g = current_city.g + graph[current_city.identifiant][child.identifiant]['weight']
            sous_graphe = graph.subgraph(list(cities_to_visit).extend([current_city.identifiant, initial_city.identifiant]))
            child.h = prims_algorithm(sous_graphe)
            child.f = child.g + child.h

            # On teste si les enfants sont déjà visités
            for closed_child in cities_already_explored:
                if child.identifiant == closed_child.identifiant:
                    continue

            # On teste si les enfants sont déjà dans la frontière.
            # Si oui, on ne les rajoute pas (pour ne pas avoir de doublons)
            for element in frontier:
                if child.identifiant == element.identifiant and child.g > element.g:
                    continue
            frontier.append(child)

        if len(frontier) > max_frontier_length:
            max_frontier_length = len(frontier)
        print("Taille maximale de la frontière = ", max_frontier_length)