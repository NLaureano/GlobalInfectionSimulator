import tkinter as tk
import random
import tkintermapview 
from PIL import Image, ImageTk

class VirusMapSimulator:
    def __init__(self, root, width=800, height=500, grid_size=20):
        self.root = root
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.rows = self.height // self.grid_size
        self.cols = self.width // self.grid_size

        # Create the Tkinter window
        self.canvas = tkintermapview.TkinterMapView(root, width=self.width, height=self.height)
        self.canvas.pack()

        #create an overlay canvas for drawing the grid
        self.overlay_canvas = tk.Canvas(root, width=self.width, height=self.height, bd=0, highlightthickness=0)
        self.overlay_canvas.pack()

        # Set an initial location and zoom level for the map
        self.canvas.set_position(0, 0)  # Center on (0, 0) - you can adjust this as needed
        self.canvas.set_zoom(2)  # Set zoom level

        # Initialize the grid for virus simulation
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]  # 0 - healthy, 1 - infected

        # Start the virus in a random location
        self.start_virus()

        # Set up simulation parameters
        self.running = False

    def start_virus(self):
        """Start by infecting a random cell in the grid."""
        initial_row = random.randint(0, self.rows - 1)
        initial_col = random.randint(0, self.cols - 1)
        self.grid[initial_row][initial_col] = 1  # 1 indicates infected

    def draw_grid(self):
        """Draw the grid on top of the map."""
        self.overlay_canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                color = "green" if self.grid[row][col] == 0 else "red"  # Green for healthy, red for infected
                # Draw a rectangle on the map based on grid size
                self.overlay_canvas.create_rectangle(
                    col * self.grid_size, row * self.grid_size,
                    (col + 1) * self.grid_size, (row + 1) * self.grid_size,
                    fill=color, outline="black"
                )

    def spread_virus(self):
        """Simulate the virus spreading to adjacent grid cells."""
        new_grid = [row[:] for row in self.grid]  # Make a copy to avoid modifying during iteration
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:  # If the cell is infected
                    # Spread to adjacent cells (up, down, left, right)
                    if row > 0 and self.grid[row - 1][col] == 0:  # Up
                        new_grid[row - 1][col] = 1
                    if row < self.rows - 1 and self.grid[row + 1][col] == 0:  # Down
                        new_grid[row + 1][col] = 1
                    if col > 0 and self.grid[row][col - 1] == 0:  # Left
                        new_grid[row][col - 1] = 1
                    if col < self.cols - 1 and self.grid[row][col + 1] == 0:  # Right
                        new_grid[row][col + 1] = 1
        self.grid = new_grid

    def start_simulation(self):
        """Start or stop the virus simulation."""
        if not self.running:
            self.running = True
            self.run_simulation()
        else:
            self.running = False

    def run_simulation(self):
        """Run the virus simulation continuously."""
        if self.running:
            self.spread_virus()
            self.draw_grid()
            self.root.after(500, self.run_simulation)  # Update every 500 ms

# Create the Tkinter window
root = tk.Tk()
root.title("Virus Map Simulator")

# Create the simulator object
simulator = VirusMapSimulator(root)

# Add a button to start/stop the simulation
start_button = tk.Button(root, text="Start/Stop Simulation", command=simulator.start_simulation)
start_button.pack()

# Initial drawing of the grid
simulator.draw_grid()

# Run the Tkinter event loop
root.mainloop()
