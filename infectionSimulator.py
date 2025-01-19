import numpy as np
import json

class InfectionSimulator:
    def __init__(self, cityCount=None, adjacenyMatrix=None):
        self.cityCount = cityCount
        self.adjacenyMatrix = adjacenyMatrix
        self.infectionVector = None
        self.cityInternalSpreadProb = None
        self.cityData = {}
        self.cityIndex = {}

    def simulateInfection(self, spreadProb=0.5, timeSteps=100):
        """
        Simulates the infection spread over a specified number of time steps.
        
        Parameters:
            spreadProb (float): Probability that an infection spreads along an edge.
            timeSteps (int): Number of simulation steps.
        """
        # Initialize infection in the first city (index 0)
        self.infectionVector[0] = 1

        # Record infection history
        infectionHistory = np.zeros((timeSteps, self.cityCount))
        infectionHistory[0] = self.infectionVector

        #For each timestep
        for t in range(1, timeSteps):
            resultingVector = np.zeros(self.cityCount)

            for i in range(self.cityCount):
                for j in range(self.cityCount):
                    if self.adjacenyMatrix[i, j] > 0:  # If nodes are connected
                        # Calculate the expected number of transmissions
                        expected_transmissions = self.infectionVector[i] * self.adjacenyMatrix[i, j] * spreadProb
                        # Determine actual new infections probabilistically
                        actual_transmissions = np.random.binomial(int(self.infectionVector[i]), self.adjacenyMatrix[i, j] * spreadProb)
                        resultingVector[j] += actual_transmissions

            # Update the infection vector
            self.infectionVector += resultingVector
            infectionHistory[t] = self.infectionVector

            print(f"Time Step {t}: {self.infectionVector}")

        return infectionHistory

    def readCityData(self):
        with open('cityinfo.json', 'r') as file:
            # Load the JSON data
            self.cityData = json.load(file)
            city_list = self.cityData['cities']
            self.cityCount = len(city_list)

            # Initialize adjacency matrix and infection vector
            self.adjacenyMatrix = np.zeros((self.cityCount, self.cityCount), dtype=float)
            self.infectionVector = np.zeros(self.cityCount)
            self.cityInternalSpreadProb = np.zeros(self.cityCount)

            # Create a dictionary to map city names to indices
            for i, city in enumerate(city_list):
                self.cityIndex[city['name']] = i

            # Populate adjacency matrix
            for city in city_list:
                rowOfCity = self.cityIndex[city['name']]
                for neighbor, distance in city['neighbors'].items():
                    colOfCity = self.cityIndex[neighbor]
                    self.adjacenyMatrix[rowOfCity][colOfCity] = 1/distance

            print("City Index Mapping:", self.cityIndex)
            print("Adjacency Matrix:\n", self.adjacenyMatrix)


# Instantiate and use the simulator
simulator = InfectionSimulator()
simulator.readCityData()
simulator.simulateInfection()
