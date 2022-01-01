import random
import numpy as np
import pydot
from hillclimbing import *
import time

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


def drawHamiltonianCircuit (distanceMatrix, circuit, filename ="solution", namePrefix="city "):
    print("DRAWING ..")
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

    graph.write_png(filename+'.png')

    print("ENDED DRAWING")




def main() :

    random.seed(5)

    num_cities = 20
    matrice = generateInstance(num_cities=num_cities, borne_inf=1, borne_sup=20)
    print("matrice distance : ")
    for i in range(len(matrice)):
        print(matrice[i])
    print("\n\n")


    tsp = TravellingSalesmanProblem(num_cities=num_cities, distanceMatrix=matrice)

    start_time = time.time()
    path = tsp.hillClimbing(randomInitState=True, log=False)
    end_time = time.time()

    print("Le temps d'execution est {:.5f} secondes".format(end_time-start_time))
    print("Best path simple hillClimbing: ")
    print(path)
    print("best cost simple hillClimbing:")
    print(tsp.stateCost(path))

    #drawHamiltonianCircuit(distanceMatrix=matrice, circuit=path, filename="hillclimbing")

    print("\n\n")
    print("RANDOM RESTART Hill climbing")
    num_iter = 10
    print("Nombre d'itérations : " , num_iter)
    start_time = time.time()
    path2 = tsp.randomRestartHillClimbing( iterations= num_iter, log=False)
    end_time = time.time()
    print("Le temps d'execution est {:.5f} secondes".format(end_time-start_time))
    
    print("Best path randomRestartHillClimbing: ")
    print(path2)
    print("best cost randomRestartHillClimbing :")
    print(tsp.stateCost(path2))

    #drawHamiltonianCircuit(distanceMatrix=matrice, circuit=path2, filename="random_restart")


if __name__ == "__main__":
    main()
