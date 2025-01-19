import tkinter as tk
from PIL import Image, ImageTk

from borders import country_borders

# Create the main window
root = tk.Tk()
root.title("World Map with Grid")

# Load the world map image (ensure you have an image file like 'Map_world.png')
image = Image.open("world.png")
photo = ImageTk.PhotoImage(image)

# Create a canvas to display the world map
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.create_image(0, 0, image=photo, anchor=tk.NW)
canvas.pack()

# Number of rows and columns for the grid
grid_rows = 100  # Adjust the number of rows based on your map resolution
grid_columns = 200  # Adjust the number of columns based on your map resolution

# Dictionary to store country borders (list of grid cell coordinates)


# Function to draw the grid on the canvas
def draw_grid():
    grid_width = image.width // grid_columns  # Calculate the width of each grid cell
    grid_height = image.height // grid_rows  # Calculate the height of each grid cell

    # Draw horizontal lines
    for i in range(1, grid_rows):
        y = i * grid_height
        canvas.create_line(0, y, image.width, y, fill="black")  # White horizontal line

    # Draw vertical lines
    for j in range(1, grid_columns):
        x = j * grid_width
        canvas.create_line(x, 0, x, image.height, fill="black")  # White vertical line

# Call the function to draw the grid
draw_grid()

def draw_borders():
    for country, cells in country_borders.items():
        for grid_x, grid_y in cells:
            cell_width = image.width // grid_columns
            cell_height = image.height // grid_rows
            x1, y1 = grid_x * cell_width, grid_y * cell_height
            x2, y2 = x1 + cell_width, y1 + cell_height
            canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black", width=1)


# List of major cities with approximate coordinates (example values)
cities = {
    "New York": (-118.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6762, 139.6503),
    "Sydney": (-33.8688, 151.2093),
    "Cairo": (30.0444, 31.2357),
    # Add more cities and their lat/lon coordinates
}

# Function to convert lat/lon to grid coordinates
def latlon_to_grid(lat, lon):
    # Assuming latitudes and longitudes range from -90 to 90 and -180 to 180 respectively
    grid_x = int((lon + 180) * (grid_columns / 360))  # Normalize longitude to grid column
    grid_y = int((90 - lat) * (grid_rows / 180))  # Normalize latitude to grid row
    return grid_x, grid_y

# Function to mark cities on the map
def mark_cities():
    for city, (lat, lon) in cities.items():
        grid_x, grid_y = latlon_to_grid(lat, lon)
        # Draw a marker (circle) on the grid at the city location
        canvas.create_oval(grid_x - 5, grid_y - 5, grid_x + 5, grid_y + 5, fill="red")  # Marker as a red circle
        # Optionally, label the city
        canvas.create_text(grid_x, grid_y - 10, text=city, fill="black", font=("Arial", 8))

# Call the function to mark cities on the grid
mark_cities()

# Function to convert grid coordinates to lat/lon
def grid_to_latlon(grid_x, grid_y):
    # Convert grid coordinates back to lat/lon
    lon = (grid_x / grid_columns) * 360 - 180  # Reverse the longitude normalization
    lat = 90 - (grid_y / grid_rows) * 180  # Reverse the latitude normalization
    return lat, lon

# Function to update the coordinates when the cursor moves
def track_grid_cursor(event):
    # Get the position of the cursor in canvas coordinates
    grid_width = image.width // grid_columns
    grid_height = image.height // grid_rows

    # Convert pixel coordinates to grid row/column
    grid_x = event.x // grid_width  # Column index
    grid_y = event.y // grid_height  # Row index

    # Ensure values stay within bounds
    grid_x = min(max(grid_x, 0), grid_columns - 1)
    grid_y = min(max(grid_y, 0), grid_rows - 1)

    # Update the label with the grid block coordinates
    coords_label.config(text=f"Grid Block: ({grid_x}, {grid_y})")

# Create a label to display the coordinates
coords_label = tk.Label(root, text="Lat: 0.00, Lon: 0.00", font=("Arial", 12), bg="white")
coords_label.pack(pady=10)

# Bind the motion event to track the cursor
canvas.bind("<Motion>", track_grid_cursor)
draw_borders()


# Start the Tkinter event loop
root.mainloop()