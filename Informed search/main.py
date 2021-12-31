from Astar import *
import networkx as nx
import matplotlib.pyplot as plt
import random


def main():
    #create a graph
    graph = nx.Graph()
    number_of_nodes = nx.path_graph(5)
    graph.add_nodes_from(number_of_nodes)
    print("number of nodes in graph: ", graph.number_of_nodes())

    #add random weighted edges
    for i in range(graph.number_of_nodes()):
        for j in range(graph.number_of_nodes()):
            if i != j:
                graph.add_edge(i, j, weight=random.randint(1, 3))
    print("number of edges in graph: ", graph.number_of_edges())

    print(graph.edges)
    #nx.draw(graph)
    #plt.show()

    print(graph.nodes())

    print("La valeur du chemin de l'arbre couvrant minimal est: ", primsAlgorithm(graph))
    path = A_star(graph)
    print(path)


if __name__ == "__main__":
    main()