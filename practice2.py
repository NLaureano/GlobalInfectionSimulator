import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("World Map with Grid")

# Load the world map image (Ensure 'Map_world.png' exists)
image = Image.open("world.png")
photo = ImageTk.PhotoImage(image)

# Create a canvas for the world map
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.create_image(0, 0, image=photo, anchor=tk.NW)
canvas.pack()

# Number of grid rows and columns
grid_rows = 100  
grid_columns = 200  

# Dictionary to store drawn borders
country_borders = {}

# List of major countries for the dropdown menu
countries_list = ["China", "UK", "Japan", "Australia", "India", "Kenya", "France", "Germany", "Brazil", "Russia", "Mexico"]

# **Dropdown menu for country selection**
selected_country = tk.StringVar()
selected_country.set(countries_list[0])  # Default selection

dropdown_menu = tk.OptionMenu(root, selected_country, *countries_list)
dropdown_menu.pack(pady=10)

# Function to draw the grid
def draw_grid():
    grid_width = image.width // grid_columns
    grid_height = image.height // grid_rows

    for i in range(1, grid_rows):
        y = i * grid_height
        canvas.create_line(0, y, image.width, y, fill="gray")

    for j in range(1, grid_columns):
        x = j * grid_width
        canvas.create_line(x, 0, x, image.height, fill="gray")

draw_grid()

# **Function to draw country borders**
def draw_borders():
    canvas.delete("borders")  # Clear old borders before redrawing
    for country, cells in country_borders.items():
        for grid_x, grid_y in cells:
            cell_width = image.width / grid_columns
            cell_height = image.height / grid_rows
            x1, y1 = grid_x * cell_width, grid_y * cell_height
            x2, y2 = x1 + cell_width, y1 + cell_height
            canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=1, tags="borders")

# **Function to add border points**
drawing_active = False  

def start_drawing(event):
    """ Start selecting border points when mouse is clicked. """
    global drawing_active
    drawing_active = True
    add_point(event)

def add_point(event):
    """ Add grid cell to country border when mouse moves while clicked. """
    if not drawing_active:
        return

    grid_width = image.width // grid_columns
    grid_height = image.height // grid_rows

    grid_x = event.x // grid_width  
    grid_y = event.y // grid_height  

    country = selected_country.get()

    if country not in country_borders:
        country_borders[country] = []

    if (grid_x, grid_y) not in country_borders[country]:
        country_borders[country].append((grid_x, grid_y))
        draw_borders()

def remove_point(event):
    """ Remove a grid cell from the selected country when right-clicked. """
    grid_width = image.width // grid_columns
    grid_height = image.height // grid_rows

    grid_x = event.x // grid_width  
    grid_y = event.y // grid_height  

    country = selected_country.get()

    if country in country_borders and (grid_x, grid_y) in country_borders[country]:
        country_borders[country].remove((grid_x, grid_y))
        draw_borders()  

def stop_drawing(event):
    """ Stop drawing when mouse is released. """
    global drawing_active
    drawing_active = False

# Bind mouse actions
canvas.bind("<Button-1>", start_drawing)  # Left click to start
canvas.bind("<B1-Motion>", add_point)  # Drag to add points
canvas.bind("<ButtonRelease-1>", stop_drawing)  # Release to stop
canvas.bind("<Button-3>", remove_point)  # Right-click to remove a point

# **Function to save drawn borders to a Python file**
def save_borders():
    """ Save country border coordinates to a file """
    with open("borders.py", "w") as f:
        f.write("country_borders = {\n")
        for country, cells in country_borders.items():
            f.write(f'    "{country}": {cells},\n')
        f.write("}\n")
    print("Borders saved to borders.py!")

# Save button
save_button = tk.Button(root, text="Save Borders", command=save_borders)
save_button.pack(pady=10)

root.mainloop()
