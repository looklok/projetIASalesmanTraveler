import random
import numpy as np
import pydot
from hillclimbing import *


def generateInstance(num_cities, borne_inf, borne_sup):
    matrice = []
    for i in range(num_cities):
        distances = []
        for j in range(num_cities):
            if j == i:
                distances.append(0)
            elif j < i:
                distances.append(matrice[j][i])
            else:
                distances.append(random.randint(borne_inf, borne_sup))
        matrice.append(distances)
    return matrice


def drawHamiltonianCircuit(distanceMatrix, circuit, namePrefix="city "):
    graph = pydot.Dot(graph_type='graph')
    path = circuit.copy()
    edgesInCircuit = set()
    for i in range(len(path)):
        edge = (path[i - 1], path[i])
        edgesInCircuit.add(edge)
        edgesInCircuit.add(edge[::-1])

    for i in range(len(distanceMatrix)):
        for j in range(len(distanceMatrix)):
            if (i, j) not in edgesInCircuit and i != j and i > j:
                weight = distanceMatrix[i][j]
                graph.add_edge(pydot.Edge(namePrefix + str(i), namePrefix + str(j), label=str(weight), style="dotted"))

    for i in range(len(path)):
        weight = distanceMatrix[path[i - 1]][path[i]]
        graph.add_edge(
            pydot.Edge(namePrefix + str(path[i - 1]), namePrefix + str(path[i]), color="red", label=str(weight)))

    graph.write_png('solution.png')


def test():
    num_cities = 5
    matrice = generateInstance(
        num_cities=num_cities, borne_inf=1, borne_sup=5
    )

    tsp = TravellingSalesmanProblem(num_cities=num_cities, distanceMatrix=matrice)
    print("matrice distance : ")
    for i in range(len(matrice)):
        print(matrice[i])
    print("random initial state : ")
    print(tsp.randomInitialState())
    print("neighbours of initial state : ")
    print(tsp.getNeighbours(tsp.initialState))

    print("state cost : ")
    print(tsp.stateCost(tsp.initialState))


def main():
    num_cities = 10
    matrice = generateInstance(
        num_cities=num_cities, borne_inf=1, borne_sup=10
    )
    print("matrice distance : ")
    for i in range(len(matrice)):
        print(matrice[i])
    tsp = TravellingSalesmanProblem(num_cities=num_cities, distanceMatrix=matrice)

    path = tsp.hillClimbing(randomInitState=True, log=True)

    print("Best path : ")
    print(path)
    print("best cost :")
    print(tsp.stateCost(path))

    drawHamiltonianCircuit(distanceMatrix=matrice, circuit=path)


if __name__ == "__main__":
    main()
