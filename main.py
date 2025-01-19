import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import infectionSimulator as sim
from borders import country_borders

class InfectionSimulator:
    def __init__(self, matrix: sim.InfectionSimulator):
        # Create the main window
        self.root = tk.Tk()
        self.matrix = matrix
        self.root.title("Infection Simulator")
        
        # Simulation state
        self.simulation_state = {
            "virulence": 50,
            "starting_country": "United States",
            "starting_infected": 1,
            "map": "default"
        }
        matrix.setInfectionVector(self.simulation_state["starting_country"], self.simulation_state["starting_infected"])
        self.infected_count = 0
        self.infected_grids = set()
        self.step_count = 0  # Step counter

        
        # Create frames
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize map
        self.setup_map()
        
        # Initialize menu
        self.setup_menu()
        
        # Initialize labels
        self.setup_labels()
    
    def update_grid(self):
        ratios = self.matrix.returnInfectionRatio()
        self.canvas.delete("nodes")
        for country in ratios:
            if country in country_borders:
                for border in country_borders[country]:
                    self.highlight_cell(border[0], border[1], ratios[country])
        self.matrix.printData()

    def setup_map(self):
        # Load and display the world map
        self.image = Image.open("world.png")
        self.photo = ImageTk.PhotoImage(self.image)
        
        # Create canvas for the map
        self.canvas = tk.Canvas(self.left_frame, width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.pack()
        
        # Grid settings
        self.grid_rows = 100
        self.grid_columns = 200
        
        # Draw grid
        self.draw_grid()
        
        # Bind mouse movement
        self.canvas.bind('<Motion>', self.track_grid_cursor)
        self.canvas.bind('<Button-1>', self.handle_click)
    
    def setup_menu(self):
        # Create menu buttons
        buttons = [
            ("Virulence", self.virulence_option),
            ("Starting Country", self.starting_country_option),
            ("Starting Infected", self.starting_infected_option),
            ("Start/Step", self.start_step_option),
            ("Reset", self.reset_option),
            ("Total Infected", self.total_infected_option)
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.right_frame, text=text, font=("Arial", 12), 
                          width=20, command=command)
            btn.pack(pady=5)
    
    def setup_labels(self):
        # Coordinates label
        self.coords_label = tk.Label(self.root, text="Lat: 0.00, Lon: 0.00", 
                                   font=("Arial", 12), bg="white")
        self.coords_label.pack(pady=10)
        
        # Total infected label
        self.total_infected_label = tk.Label(self.root, text="Total Infected: 0", 
                                           font=("Arial", 12))
        self.total_infected_label.pack(pady=10)

        # Step count label
        self.step_label = tk.Label(self.root, text="Steps: 0", font=("Arial", 12))
        self.step_label.pack(pady=10)


    
    def draw_grid(self):
        grid_width = self.image.width // self.grid_columns
        grid_height = self.image.height // self.grid_rows
        
        # Draw horizontal lines
        for i in range(1, self.grid_rows):
            y = i * grid_height
            self.canvas.create_line(0, y, self.image.width, y, fill="black")
        
        # Draw vertical lines
        for j in range(1, self.grid_columns):
            x = j * grid_width
            self.canvas.create_line(x, 0, x, self.image.height, fill="black")
    
    def track_grid_cursor(self, event):
        grid_x = event.x // (self.image.width // self.grid_columns)
        grid_y = event.y // (self.image.height // self.grid_rows)
        
        # Convert grid coordinates to lat/lon
        lat, lon = self.grid_to_latlon(grid_x, grid_y)
        self.coords_label.config(text=f"Lat: {lat:.2f}, Lon: {lon:.2f}")
    
    def handle_click(self, event):
        grid_x = event.x // (self.image.width // self.grid_columns)
        grid_y = event.y // (self.image.height // self.grid_rows)
        
        # Add to infected grids if in simulation mode
        if self.simulation_state["starting_country"] is None:
            self.infected_grids.add((grid_x, grid_y))
            self.update_infected_count()
            self.highlight_cell(grid_x, grid_y)
    
    def highlight_cell(self, grid_x, grid_y, ratio=0.0):
        cell_width = self.image.width // self.grid_columns
        cell_height = self.image.height // self.grid_rows
        x1, y1 = grid_x * cell_width, grid_y * cell_height
        x2, y2 = x1 + cell_width, y1 + cell_height
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=("#%02x%02x%02x" % (min(255, int(ratio * 255) + 51), 129, 195)), outline="black", width=1, tags="nodes")
    
    def grid_to_latlon(self, grid_x, grid_y):
        lat = 90 - (grid_y * 180 / self.grid_rows)
        lon = -180 + (grid_x * 360 / self.grid_columns)
        return lat, lon
    
    def update_infected_count(self):
        self.infected_count = self.matrix.getInfectedCount()
        self.total_infected_label.config(text=f"Total Infected: {self.infected_count}")
    
    # Menu option functions
    def virulence_option(self):
        window = tk.Toplevel(self.root)
        window.title("Adjust Virulence")
        window.geometry("300x200")
        
        label = tk.Label(window, text="Adjust the virulence:", font=("Arial", 12))
        label.pack(pady=10)
        
        def update_virulence(value):
            virulence_label.config(text=f"Virulence: {value}%")
            self.simulation_state["virulence"] = int(value)
        
        slider = tk.Scale(window, from_=0, to=100, orient="horizontal", 
                         font=("Arial", 12), command=update_virulence)
        slider.set(self.simulation_state["virulence"])
        self.matrix.setSpreadProb(self.simulation_state["virulence"])
        slider.pack(pady=10)
        
        virulence_label = tk.Label(window, text=f"Virulence: {self.simulation_state['virulence']}%", 
                                  font=("Arial", 12))
        virulence_label.pack(pady=10)

        def confirm_virulence():
            selected_virulence = slider.get()
            messagebox.showinfo("Virulence Selected", f"You selected{selected_virulence}%virulence.")

        def exit_virulence():
            window.destroy()

        confirm_button = tk.Button(window, text="Confirm", font=("Arial", 12), command=confirm_virulence)
        confirm_button.pack(side=tk.LEFT, padx=20, pady=10)

        exit_button = tk.Button(window, text="Exit", command=exit_virulence)
        exit_button.pack(side=tk.RIGHT, padx=20, pady=10)
        
    
    def starting_country_option(self):
        window = tk.Toplevel(self.root)
        window.title("Select Starting Country")
        window.geometry("300x400")

        countries = list(country_borders.keys())

        label = tk.Label(window, text="Select a country to start infection:", font=("Arial, 12"))
        label.pack(pady=10)

        listbox = tk.Listbox(window, height=15, font=("Arial", 12))
        for country in countries:
            listbox.insert(tk.END, country)  # Insert each country into the Listbox
        listbox.pack(pady=10)

        def select_country():
            selected_country = listbox.get(tk.ACTIVE)
            messagebox.showinfo("Selected Country", f"You selected {selected_country} as the starting country.")

        def exit_country():
            window.destroy()

        # Button to confirm the selection
        select_button = tk.Button(window, text="Select", font=("Arial", 12), command=select_country)
        select_button.pack(side=tk.LEFT, padx=20, pady=10)

        exit_button = tk.Button(window, text="Exit", command=exit_country)
        exit_button.pack(side=tk.RIGHT, padx=20, pady=10)


    def starting_infected_option(self):
        window = tk.Toplevel(self.root)
        window.title("Set Starting Infected")
        window.geometry("300x200")
        
        label = tk.Label(window, text="Enter number of initially infected:", 
                        font=("Arial", 12))
        label.pack(pady=10)
        
        entry = tk.Entry(window, font=("Arial", 12))
        entry.insert(0, str(self.simulation_state["starting_infected"]))
        entry.pack(pady=10)
        
        def update_infected():
            try:
                value = int(entry.get())
                if value >= 0:
                    self.simulation_state["starting_infected"] = value
                    self.matrix.setInfectionVector(self.simulation_state["starting_country"], self.simulation_state["starting_infected"])
                    window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter a positive number")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        button = tk.Button(window, text="Set", command=update_infected, 
                          font=("Arial", 12))
        button.pack(pady=10)
    
    def start_step_option(self):
        # Add simulation step logic here
        self.step_count += 1 
        self.matrix.step()
        self.update_grid()
        self.step_label.config(text=f"Steps: {self.step_count}")
        self.total_infected_label.config(text=f"Total Infected: {self.matrix.getInfectedCount()}")
    
    def reset_option(self):
        #self.infected_grids.clear()
        self.update_infected_count()
        self.matrix.reset()
        self.matrix.setInfectionVector(self.simulation_state["starting_country"], self.simulation_state["starting_infected"])
        self.update_grid()
        # Clear highlighted cells
        #self.setup_map()
    
    def total_infected_option(self):
        messagebox.showinfo("Total Infected", 
                          f"Current total infected: {self.matrix.getInfectedCount()}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulator = InfectionSimulator()
    simulator.run()
