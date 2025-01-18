import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("World Map with Grid")

# Load the world map image (ensure you have an image file like 'world_map.jpg')
image = Image.open("world_map.jpg")
photo = ImageTk.PhotoImage(image)

# Create a canvas to display the world map
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.create_image(0, 0, image=photo, anchor=tk.NW)
canvas.pack()

# Number of rows and columns for the grid
grid_rows = 100  # Adjust the number of rows based on your map resolution
grid_columns = 200 # Adjust the number of columns based on your map resolution

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

# Start the Tkinter event loop
root.mainloop()
