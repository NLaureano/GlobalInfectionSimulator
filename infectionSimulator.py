import numpy as np

class InfectionSimulator:
    def __init__(self, cityCount, adjacenyMatrix):
        self.cityCount = cityCount
        self.adjacenyMatrix = adjacenyMatrix
        self.infectionVector = np.zeros(cityCount)
        
    #Simulate the infection
    def simulateInfection(self):
        #Initial infection
        self.infectionVector[0] = 1

        #Simulate the infection
        for i in range(1, 10):
            print(self.infectionVector)
            np.matmul(self.adjacenyMatrix, self.infectionVector, self.infectionVector)

simulator = InfectionSimulator()
simulator.simulateInfection()