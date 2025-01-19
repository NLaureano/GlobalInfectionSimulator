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
        self.countryTravelScore = None #Travel score of each country
        self.countryData = {} #Json loaded into memory
        self.countryIndex = {} #Index of each country in the adjacency matrix\
        self.spreadProb = 0.5

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
        infectionHistory = np.zeros((timeSteps, self.countryCount))
        infectionHistory[0] = self.infectionVector

        #For each timestep
        for t in range(1, timeSteps):
            infectionHistory[t] = self.step(spreadProb)

            print(f"Time Step {t}: {self.infectionVector}")

        return infectionHistory
    
    def step(self):
        resultingVector = np.zeros(self.countryCount)
        for i in range(self.countryCount):
            for j in range(self.countryCount):
                if self.adjacenyMatrix[i, j] > 0:  # If nodes are connected
                    # Determine actual new infections probabilistically
                    actual_transmissions = np.random.binomial(int(self.infectionVector[i]), self.adjacenyMatrix[i, j] * self.spreadProb)
                    resultingVector[j] += actual_transmissions

        # Update the infection vector
        self.infectionVector += resultingVector
        self.infectionVector = np.minimum(self.infectionVector, self.populationVector)
        # Apply country response to reduce infections
        self.infectionVector = self.applyCountryResponse(self.infectionVector)

        self.infectionVector = np.minimum(self.infectionVector, self.populationVector)  # Cap infections at population size
        return self.infectionVector
    
    def applyCountryResponse(self, current_infections):
        """
        Models how countries respond to and fight the infection based on their HDI.
        
        Parameters:
            current_infections: Current infection vector
            
        Returns:
            Updated infection vector after country response
        """
        # Convert HDI to response effectiveness (0 to 1)
        # Higher HDI means better response, but not perfect
        response_effectiveness = self.countryHDI * 0.3  # Max 30% effectiveness to prevent immediate containment
        
        # Calculate reduction based on current infections and HDI
        # More infections = stronger response
        infection_ratio = current_infections / self.populationVector
        infection_ratio = np.nan_to_num(infection_ratio, 0)  # Handle division by zero
        
        # Response strength increases with infection ratio
        response_strength = infection_ratio * response_effectiveness
        
        # Calculate reduced infections
        reduction = current_infections * response_strength
        
        # Ensure we don't reduce below 0 and apply randomness
        # Countries might have varying success in their response
        reduction = np.random.binomial(reduction.astype(int), 0.8)  # 80% chance of successful reduction
        
        return np.maximum(current_infections - reduction, 0)

    def returnInfectionRatio(self):
        res = {}
        for country in self.countryData:
            res[country['name']] = self.infectionVector[self.countryIndex[country['name']]] / self.populationVector[self.countryIndex[country['name']]]
        return res
    
    def setInfectionVector(self, startCountry="United States", startInfections="1"):
        print(self.countryIndex)
        self.infectionVector[self.countryIndex[startCountry]] = startInfections

    def setSpreadProb(self, spreadProb):
        self.spreadProb = spreadProb

    def reset(self, neighborPriority=0.1, spreadProb=0.5):
        with open('datasets/seed.json', 'r') as file:
            # Load the JSON data
            self.countryData = json.load(file)
            self.countryCount = len(self.countryData)
            self.populationVector = np.zeros(self.countryCount) #Population of each country
            self.countryHDI = np.zeros(self.countryCount) #Human Development Index of each country
            self.countryTravelScore = np.zeros(self.countryCount) #Travel score of each country
            self.countryIndex = {}

            # Initialize adjacency matrix and infection vector
            self.adjacenyMatrix = np.zeros((self.countryCount, self.countryCount), dtype=float)
            self.infectionVector = np.zeros(self.countryCount)

            # Create a dictionary to map city names to indices
            for i, country in enumerate(self.countryData):
                self.countryIndex[country['name']] = i
                #print(f"Country {country['name']} has index {i}")

            sumTravelScore = 0
            for country in self.countryData:
                #print("Country PASSANGER:", country['name'])
                sumTravelScore += country['annual_passenger_traffic']
            #print("Sum of travel scores:", sumTravelScore)

            # Populate population, HDI, and travel score vectors
            for country in self.countryData:
                #print("Country updating:", country['name'])
                self.populationVector[self.countryIndex[country['name']]] = country['population']
                self.countryHDI[self.countryIndex[country['name']]] = country['hdi']
                self.countryTravelScore[self.countryIndex[country['name']]] = country['annual_passenger_traffic'] / sumTravelScore
            
            # print("Population Vector:", self.populationVector)
            # print("HDI Vector:", self.countryHDI)
            # print("Travel Score Vector:", self.countryTravelScore)

            # Populate adjacency matrix
            for country in self.countryData:
                rowOfCountry = self.countryIndex[country['name']]
                for i in range(self.countryCount):
                    self.adjacenyMatrix[rowOfCountry][i] = self.countryTravelScore[i]
                for neighbor in country['neighbors']:
                    if neighbor not in self.countryIndex:
                        continue
                    colOfCountry = self.countryIndex[neighbor]
                    self.adjacenyMatrix[rowOfCountry][colOfCountry] += neighborPriority
                self.adjacenyMatrix[rowOfCountry] = self.softmax(self.adjacenyMatrix[rowOfCountry])

            print("City Index Mapping:", self.countryIndex)
            print("Adjacency Matrix:\n", self.adjacenyMatrix)

    def softmax(self, x):
    # """
    # Compute the softmax of a 1D or 2D array.

    # Parameters:
    # - x: numpy array, shape (n,) for 1D or (m, n) for 2D

    # Returns:
    # - numpy array with the same shape as x, containing softmax probabilities
    # """
    # For numerical stability, subtract the maximum value in each row or the array itself
        if x.ndim == 1:
            max_val = np.max(x)
            exp_x = np.exp(x - max_val)
            return exp_x / np.sum(exp_x)
        elif x.ndim == 2:
            max_vals = np.max(x, axis=1, keepdims=True)
            exp_x = np.exp(x - max_vals)
            return exp_x / np.sum(exp_x, axis=1, keepdims=True)
        else:
            raise ValueError("Input array must be 1D or 2D.")

# Instantiate and use the simulator
#simulator = InfectionSimulator()
#simulator.reset()
#simulator.simulateInfection(0.5, 100)
#simulator.simulateInfection()
