import infectionSimulator as sim
import main 
import borders

# Run the simulation
simMatrix = sim.InfectionSimulator()
simMatrix.reset()
simMatrix.printData()
simulator = main.InfectionSimulator(simMatrix)
simulator.run()