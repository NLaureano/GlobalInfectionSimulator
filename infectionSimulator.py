import numpy as np
import json



#Country count = The amount of countries simulated
#Adjacency matrix = The matrix that shows the weighted connections between countries
#Infection vector = The vector that shows the amount of infected people in each country
#CountryHDI = The Human Development Index of each country
#CountryData = The data of each country in a dictionary
#CountryIndex = The index of each country in the adjacency matrix
class InfectionSimulator:
    def __init__(self, countryCount=None, adjacenyMatrix=None):
        self.countryCount = countryCount
        self.adjacenyMatrix = adjacenyMatrix
        self.infectionVector = None #Number of infected people in each country
        self.populationVector = None #Population of each country
        self.countryHDI = None #Human Development Index of each country
        self.countryData = {}
        self.countryIndex = {}

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
                        # Determine actual new infections probabilistically
                        actual_transmissions = np.random.binomial(int(self.infectionVector[i]), self.adjacenyMatrix[i, j] * spreadProb)
                        resultingVector[j] += actual_transmissions

            # Update the infection vector
            self.infectionVector += resultingVector
            infectionHistory[t] = self.infectionVector

            print(f"Time Step {t}: {self.infectionVector}")

        return infectionHistory
    
    def step(self):
        pass

    def reset(self):
        with open('datasets/seed.json', 'r') as file:
            # Load the JSON data
            self.countryData = json.load(file)
            country_list = self.countryData
            self.countryCount = len(country_list)

            # Initialize adjacency matrix and infection vector
            self.adjacenyMatrix = np.zeros((self.countryCount, self.countryCount), dtype=float)
            self.infectionVector = np.zeros(self.countryCount)

            # Create a dictionary to map city names to indices
            for i, country in enumerate(country_list):
                self.countryIndex[country['name']] = i

            # Populate adjacency matrix
            for country in country_list:
                rowOfCountry = self.countryIndex[country['name']]
                for neighbor, proximityScore in country['neighbors'].items():
                    colOfCountry = self.countryIndex[neighbor]
                    self.adjacenyMatrix[rowOfCountry][colOfCountry] = proximityScore

            print("City Index Mapping:", self.countryIndex)
            print("Adjacency Matrix:\n", self.adjacenyMatrix)


# Instantiate and use the simulator
simulator = InfectionSimulator()
simulator.readCityData()
simulator.simulateInfection()
