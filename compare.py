import hill_climbing.hillclimbing as hill
import Informed_search.Astar as informed
import random
import math
from numpy import *
import networkx as nx
from matplotlib.pyplot import *
import time


class Ville:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, ville):
        distance = math.sqrt((math.pow(ville.x - self.x, 2)) + (math.pow(ville.y - self.y, 2)))
        return distance


class Individu:
    # cree un circuit vide
    def __init__(self, individu=None):
        self.individu = []
        self.efficacite = 0.0
        self.distance = 0
        if individu is not None:
            self.individu = individu
        else:
            for i in range(0, len(Villes)):
                self.individu.append(None)

    def __getitem__(self, index):
        return self.individu[index]

    def getVille(self, pos):
        return self.individu[pos]

    def setVille(self, pos, ville):
        self.individu[pos] = ville
        self.efficacite = 0.0
        self.distance = 0

    def tailleIndividu(self):
        return len(self.individu)

    def contientVille(self, ville):
        return ville in self.individu

    # cree un circuit avec toutes les villes et le melange
    def genererIndividu(self):
        for indiceVille in range(0, len(Villes)):
            self.setVille(indiceVille, Villes[indiceVille])
        random.shuffle(self.individu)

    # renvoie la valeur d efficacite du circuit
    # plus la distance du circuit est faible et plus la valeur renvoyee sera elevee
    def getEfficacite(self):
        if self.efficacite == 0:
            self.efficacite = 1 / float(self.getDistance())
        return self.efficacite

    # calcule la somme des distances entre les villes
    def getDistance(self):
        if self.distance == 0:
            distanceTot = 0
            for indiceVille in range(0, len(self.individu)):
                villeOrigine = self.getVille(indiceVille)
                villeArrivee = self.getVille(0)
                if indiceVille + 1 < len(self.individu):
                    villeArrivee = self.getVille(indiceVille + 1)
                else:
                    villeArrivee = self.getVille(0)
                distanceTot += villeOrigine.distance(villeArrivee)
            self.distance = distanceTot
        return self.distance


class Population:
    # Cree un ensemble de circuit
    def __init__(self, taillePopulation, init):
        self.circuits = []
        for i in range(0, taillePopulation):
            self.circuits.append(None)
        if init:
            for i in range(0, taillePopulation):
                nouveauCircuit = Individu()
                nouveauCircuit.genererIndividu()
                self.circuits[i] = nouveauCircuit

    # Calcule le circuit le plus efficace
    def getMeilleur(self):
        meilleur = self.circuits[0]
        for i in range(0, len(self.circuits)):
            if meilleur.getEfficacite() <= self.circuits[i].getEfficacite():
                meilleur = self.circuits[i]
        return meilleur


def evoluerPopulation(pop):
    nouvellePopulation = Population(len(pop.circuits), False)
    nouvellePopulation.circuits[0] = pop.getMeilleur()

    for i in range(1, len(nouvellePopulation.circuits)):
        parent1 = selectionVillesParents(pop)
        parent2 = selectionVillesParents(pop)
        enfant = croisement(parent1, parent2)
        nouvellePopulation.circuits[i] = enfant

    for i in range(1, len(nouvellePopulation.circuits)):
        mutation(nouvellePopulation.circuits[i])

    return nouvellePopulation


def croisement(parent1, parent2):
    enfant = Individu()
    borne1 = int(random.random() * parent1.tailleIndividu())
    borne2 = int(random.random() * parent1.tailleIndividu())

    for i in range(0, enfant.tailleIndividu()):
        if borne1 < borne2 and borne1 < i < borne2:
            enfant.setVille(i, parent1.getVille(i))
        elif borne1 > borne2:
            if not (borne1 > i > borne2):
                enfant.setVille(i, parent1.getVille(i))

    for i in range(0, parent2.tailleIndividu()):
        if not enfant.contientVille(parent2.getVille(i)):
            for ii in range(0, enfant.tailleIndividu()):
                if enfant.getVille(ii) is None:
                    enfant.setVille(ii, parent2.getVille(i))
                    break
    return enfant


def selectionVillesParents(pop):
    selec = Population(nbVillesaComparer, False)
    for i in range(0, nbVillesaComparer):
        randomId = int(random.random() * len(pop.circuits))
        selec.circuits[i] = pop.circuits[randomId]
    meilleur = selec.getMeilleur()
    return meilleur


def mutation(circuit):
    for circuitPos1 in range(0, circuit.tailleIndividu()):
        if random.random() < tauxMutation:
            circuitPos2 = int(circuit.tailleIndividu() * random.random())

            ville1 = circuit.getVille(circuitPos1)
            ville2 = circuit.getVille(circuitPos2)

            circuit.setVille(circuitPos2, ville1)
            circuit.setVille(circuitPos1, ville2)


def citiesToDistanceMatrix(villes):
    matrice = []
    for i in range(len(villes)):
        distances = []
        for j in range(len(villes)):
            if j == i:
                distances.append(0)
            elif j < i:
                distances.append(matrice[j][i])
            else:
                dis = villes[i].distance(villes[j])
                distances.append(dis)
        matrice.append(distances)

    return matrice


def villes_aleatoires():
    random.seed(12)
    tabz = around(random.rand(nbvilles, 2) * 100)
    for i in range(0, nbvilles):
        Villes.append(Ville(tabz[i][0], tabz[i][1]))


def matrixToGraph(matrice):
    graph = nx.Graph()
    number_of_nodes = nx.path_graph(len(matrice))
    graph.add_nodes_from(number_of_nodes)
    # print("number of nodes in graph: ", graph.number_of_nodes())

    # add random weighted edges
    for i in range(graph.number_of_nodes()):
        for j in range(graph.number_of_nodes()):
            if i != j:
                graph.add_edge(i, j, weight=matrice[i][j])

    # print("number of edges in graph: ", graph.number_of_edges())

    # print(graph.edges)
    return graph


if __name__ == '__main__':

    Villes = []
    nbvilles = 5
    distancesTots = []
    nbpops = 4  # nbpop doit être inférieur à nbvilles. from_=0, to=100
    nbtours = 200  # from_=0, to=500
    tauxMutation = 0.3  # from_=0, to=0.5
    nbVillesaComparer = 3  # doit être inférieur à nbvilles. from_=0, to=20

    villes_aleatoires()
    """for v in Villes :
        print(v.x , v.y)"""

    matrice = citiesToDistanceMatrix(Villes)
    """for i in range(len(matrice)):
        print(matrice[i])"""

    graph = matrixToGraph(matrice)

    pop = Population(nbpops, True)
    print("GENETIC ALGO : ")
    print("Distance initiale : " + str(pop.getMeilleur().getDistance()))

    distancesTots.append(pop.getMeilleur().getDistance())
    start_time = time.time()
    popFinales = evoluerPopulation(pop)

    for i in range(0, nbtours):
        popFinales = evoluerPopulation(popFinales)
        distancesTots.append(popFinales.getMeilleur().getDistance())

    meilleurePopulation = popFinales.getMeilleur()
    end_time = time.time()
    print("Le temps d'exécution est de {:.5f} secondes".format(end_time - start_time))

    print("Distance finale : " + str(meilleurePopulation.getDistance()))
    path0 = []
    for v in meilleurePopulation.individu:
        path0.append(Villes.index(v))
    print("path : ", path0)
    print("\n")

    tsp = hill.TravellingSalesmanProblem(num_cities=nbvilles, distanceMatrix=matrice)

    print("HILL CLIMBING : ")
    start_time = time.time()
    path = tsp.hillClimbing(randomInitState=True, log=False)
    end_time = time.time()

    print("Le temps d'exécution est de {:.5f} secondes".format(end_time - start_time))
    print("Best path simple hillClimbing : ", path)
    print("Best cost simple hillClimbing : ", tsp.stateCost(path))

    print("\n")
    print("RANDOM RESTART HILL CLIMBING :")
    num_iter = 10
    print("Nombre d'itérations : ", num_iter)
    start_time = time.time()
    path2 = tsp.randomRestartHillClimbing(iterations=num_iter, log=False)
    end_time = time.time()
    print("Le temps d'execution est de {:.5f} secondes".format(end_time - start_time))

    print("Best path randomRestartHillClimbing: ", path2)
    print("Best cost randomRestartHillClimbing :", tsp.stateCost(path2))

    print("\n")
    print("A STAR : ")

    start_time = time.time()
    path3 = informed.A_star(graph, log=False)
    end_time = time.time()

    print("Le temps d'execution est {:.5f} secondes".format(end_time - start_time))

    print("Circuit hamiltonien : ", path3)
    print("Coût total : ", tsp.stateCost(path3))
