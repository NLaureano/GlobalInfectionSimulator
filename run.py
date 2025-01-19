import infectionSimulator as sim
import main 
import borders

# Run the simulation
simMatrix = sim.InfectionSimulator()
simulator = main.InfectionSimulator(simMatrix)
simulator.run()