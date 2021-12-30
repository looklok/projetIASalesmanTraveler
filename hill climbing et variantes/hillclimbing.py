import random
import numpy as np


class TravellingSalesmanProblem:
    def __init__(self, num_cities, distanceMatrix) -> None:
        self.distanceMatrix = distanceMatrix
        self.num_cities = num_cities
        self.initialState = None

    def randomInitialState(self):
        cities = list(range(self.num_cities))
        state = []
        for i in range(self.num_cities):
            nextCity = cities.pop(random.randint(0, len(cities) - 1))
            state.append(nextCity)

        self.initialState = state
        return state

    def stateCost(self, state):
        cost = 0
        for i in range(len(state)):
            cost += self.distanceMatrix[state[i - 1]][state[i]]

        return cost

    def getNeighbours(self, state):
        neighbours = []
        s = state.copy()
        startState = s[0]
        s.append(startState)
        for i in range(1, len(s) - 2):
            for j in range(i + 2, len(s)):
                new_neighbour = s[:]
                new_neighbour[i:j] = s[j - 1:i - 1:-1]

                neighbours.append(new_neighbour[:-1])

        return neighbours

    def bestNeighbour(self, state):
        min_cost = np.Infinity
        best_neighbour = None
        neighbours = self.getNeighbours(state)
        for n in neighbours:
            cost = self.stateCost(n)
            if cost < min_cost:
                min_cost = cost
                best_neighbour = n

        return best_neighbour

    def hillClimbing(self, randomInitState=True, log=False):
        if randomInitState:
            self.initialState = self.randomInitialState()
        current_state = self.initialState
        current_cost = self.stateCost(self.initialState)
        if log:
            print("random initial state : {} with cost {}".format(self.initialState, current_cost))

        while True:
            best_neighbour = self.bestNeighbour(current_state)
            best_cost = self.stateCost(best_neighbour)
            if best_cost >= current_cost:
                return current_state
            else:
                if log:
                    print("Better neighbour : {}  with cost {}".format(best_neighbour, best_cost))
                    print("Gain of : {}\n".format(current_cost - best_cost))
                    current_state = best_neighbour
                    current_cost = best_cost
