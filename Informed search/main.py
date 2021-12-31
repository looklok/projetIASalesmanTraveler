from Astar import *
import networkx as nx
import matplotlib.pyplot as plt
import random
import pydot

def drawHamiltonianCircuitFromGraph (graphe, circuit, filename ="solution", namePrefix="city "):
    print("DRAWING ..")
    graph = pydot.Dot(graph_type='graph')
    path = circuit[:-1].copy()
    edgesInCircuit = set()
    for i in range(len(path)):
        edge = (path[i - 1], path[i])
        edgesInCircuit.add(edge)
        edgesInCircuit.add(edge[::-1])

    for i,j in graphe.edges :
        if (i, j) not in edgesInCircuit and i != j :
            weight = graphe[i][j]["weight"]
            graph.add_edge(pydot.Edge(namePrefix + str(i), namePrefix + str(j), label=str(weight), style="dotted"))

    for i in range(len(path)):
        weight = graphe[path[i - 1]][path[i]]["weight"]
        graph.add_edge(pydot.Edge(namePrefix + str(path[i - 1]), namePrefix + str(path[i]), color="red", label=str(weight)))

    graph.write_png(filename+'.png')

    print("ENDED DRAWING")


def main():
    #create a graph

    random.seed(12)

    graph = nx.Graph()
    number_of_nodes = nx.path_graph(8)
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

    #print(graph.nodes())

    #print("La valeur du chemin de l'arbre couvrant minimal est: ", primsAlgorithm(graph))
    path = A_star(graph)
    print("Circuit hamiltonien", path)

    drawHamiltonianCircuitFromGraph(graphe=graph, circuit=path, filename="astar")


if __name__ == "__main__":
    main()