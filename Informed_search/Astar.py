import random as rd
import networkx as nx


class City:
    def __init__(self, identifiant: int, parent=None):
        self.parent = parent
        self.identifiant = identifiant
        self.g = 0
        self.h = 0
        self.f = 0
        self.to_visit = []
    def __eq__(self, other) -> bool:
        return self.identifiant == other.identifiant and self.to_visit == other.to_visit 


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


def A_star(graph, log=False):

    frontier = []
    explored = []

    initial_city = City(rd.randint(0, len(graph.nodes())-1), parent=None)
    cities_to_visit = [initial_city.identifiant]
    for n in graph.nodes():
        cities_to_visit.append(n)

    initial_city.to_visit = cities_to_visit
   
   
    frontier.append(initial_city)

    while len(frontier) > 0:
        current_city = frontier[0]
        current_index = 0
        for index, item in enumerate(frontier):
            if item.f < current_city.f:
                current_city = item
                current_index = index

        frontier.pop(current_index)
        explored.append(current_city)



        
        current_city.to_visit.remove(current_city.identifiant)
        #print("To visit :  ", current_city.to_visit)
        # Found the goal
        if current_city.identifiant == initial_city.identifiant and len(current_city.to_visit) == 0:
            print("Taille de la frontière = ", len(frontier))
            path = []
            current = current_city
            while current is not None:
                path.append(current.identifiant)
                current = current.parent
            return path

        # Generate children
        children = []
        for id in current_city.to_visit:
            if id != current_city.identifiant:
                city = City(identifiant=id, parent=current_city)
                city.to_visit  = current_city.to_visit.copy()
                children.append(city)

        # Loop through children
        for child in children:
            # Create the f, g, and h values
            child.g = current_city.g + graph[current_city.identifiant][child.identifiant]['weight']
            sous_graphe = graph.subgraph(list(cities_to_visit).extend([child.identifiant]))
            child.h = prims_algorithm(sous_graphe)
            child.f = child.g + child.h

            # On teste si les enfants sont déjà visités
            for node in explored:
                if child == node:
                    continue

            # On teste si les enfants sont déjà dans la frontière.
            # Si oui, on ne les rajoute pas (pour ne pas avoir de doublons)
            for element in frontier:
                if child == element:
                    continue

            frontier.append(child)
        if log:
            print("Taille de la frontière = ", len(frontier))