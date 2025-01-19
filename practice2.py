import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("World Map with Grid")

# Load the world map image (Ensure 'world.png' exists)
original_image = Image.open("world.png")
zoom_level = 1.0
photo = ImageTk.PhotoImage(original_image)

# Create a canvas for the world map with scrollbars
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(canvas_frame, xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set, width=800, height=600)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

h_scroll.config(command=canvas.xview)
v_scroll.config(command=canvas.yview)

canvas_image = canvas.create_image(0, 0, image=photo, anchor=tk.NW)
canvas.config(scrollregion=canvas.bbox("all"))

# Number of grid rows and columns
grid_rows = 100
grid_columns = 200

# Dictionary to store drawn borders
country_borders = {}

# List of major countries for the dropdown menu
countries_list = ["USA", "China", "UK", "Japan", "Australia", "India", "Kenya", "France", "Germany", "Brazil", "Russia", "Mexico"]

# Dropdown menu for country selection
selected_country = tk.StringVar()
selected_country.set(countries_list[0])  # Default selection

dropdown_menu = tk.OptionMenu(root, selected_country, *countries_list)
dropdown_menu.pack(pady=10)

# Function to redraw the grid after resizing
def draw_grid():
    grid_width = int((original_image.width * zoom_level) / grid_columns)
    grid_height = int((original_image.height * zoom_level) / grid_rows)

    canvas.delete("grid")  # Remove old grid
    for i in range(1, grid_rows):
        y = i * grid_height
        canvas.create_line(0, y, original_image.width * zoom_level, y, fill="gray", tags="grid")
    for j in range(1, grid_columns):
        x = j * grid_width
        canvas.create_line(x, 0, x, original_image.height * zoom_level, fill="gray", tags="grid")

# Function to redraw country borders after resizing
def draw_borders():
    canvas.delete("borders")  # Clear old borders
    for country, cells in country_borders.items():
        for grid_x, grid_y in cells:
            cell_width = int((original_image.width * zoom_level) / grid_columns)
            cell_height = int((original_image.height * zoom_level) / grid_rows)
            x1, y1 = grid_x * cell_width, grid_y * cell_height
            x2, y2 = x1 + cell_width, y1 + cell_height
            canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=1, tags="borders")

# Function to handle zoom in/out
def zoom(event):
    global photo, zoom_level
    if event.delta > 0:  # Zoom in
        zoom_level *= 1.2
    elif event.delta < 0:  # Zoom out
        zoom_level /= 1.2

    # Resize image
    new_width = int(original_image.width * zoom_level)
    new_height = int(original_image.height * zoom_level)
    resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)

    # Update canvas image
    canvas.itemconfig(canvas_image, image=photo)
    canvas.config(scrollregion=canvas.bbox("all"))
    draw_grid()
    draw_borders()

# Bind mouse actions for zoom
canvas.bind("<MouseWheel>", zoom)

# Functions for adding/removing points
drawing_active = False

def start_drawing(event):
    """Start selecting border points when mouse is clicked."""
    global drawing_active
    drawing_active = True
    add_point(event)

def add_point(event):
    """Add grid cell to country border when mouse moves while clicked."""
    if not drawing_active:
        return

    grid_width = int((original_image.width * zoom_level) / grid_columns)
    grid_height = int((original_image.height * zoom_level) / grid_rows)

    grid_x = int(event.x // grid_width)
    grid_y = int(event.y // grid_height)

    country = selected_country.get()
    if country not in country_borders:
        country_borders[country] = []
    if (grid_x, grid_y) not in country_borders[country]:
        country_borders[country].append((grid_x, grid_y))
        draw_borders()

def remove_point(event):
    """Remove a grid cell from the selected country when right-clicked."""
    grid_width = int((original_image.width * zoom_level) / grid_columns)
    grid_height = int((original_image.height * zoom_level) / grid_rows)

    grid_x = int(event.x // grid_width)
    grid_y = int(event.y // grid_height)

    country = selected_country.get()
    if country in country_borders and (grid_x, grid_y) in country_borders[country]:
        country_borders[country].remove((grid_x, grid_y))
        draw_borders()

def stop_drawing(event):
    """Stop drawing when mouse is released."""
    global drawing_active
    drawing_active = False

# Bind mouse actions
canvas.bind("<Button-1>", start_drawing)  # Left click to start
canvas.bind("<B1-Motion>", add_point)  # Drag to add points
canvas.bind("<ButtonRelease-1>", stop_drawing)  # Release to stop
canvas.bind("<Button-3>", remove_point)  # Right-click to remove a point

# Save borders to a file
def save_borders():
    with open("borders.py", "w") as f:
        f.write("country_borders = {\n")
        for country, cells in country_borders.items():
            f.write(f'    "{country}": {cells},\n')
        f.write("}\n")
    print("Borders saved to borders.py!")

# Save button
save_button = tk.Button(root, text="Save Borders", command=save_borders)
save_button.pack(pady=10)

# Initial grid and borders
draw_grid()

# Run the Tkinter main loop
root.mainloop()