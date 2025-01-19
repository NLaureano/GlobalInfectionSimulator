import tkinter as tk
from tkinter import messagebox

# Function to show information or perform actions
def virulence_option():
    messagebox.showinfo("Virulence", "This will adjust the virulence of the disease.")

def starting_country_option():
    messagebox.showinfo("Starting Country", "Select the starting country for the disease.")

def starting_infected_option():
    messagebox.showinfo("Starting Infected", "Specify the number of starting infected individuals.")

def start_step_option():
    messagebox.showinfo("Start/Step", "Start the simulation or move to the next step.")

def reset_option():
    messagebox.showinfo("Reset", "This will reset the simulation.")

def total_infected_option():
    messagebox.showinfo("Total Infected", "This will show the total number of infected individuals.")

# Create the main window
root = tk.Tk()
root.title("Infectious Disease Simulation Menu")
root.geometry("400x400")  # Adjust window size for the menu

# Title Label
title_label = tk.Label(root, text="Infectious Disease Simulation", font=("Arial", 16), fg="blue")
title_label.pack(pady=10)

# Left frame for the menu
menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

# Buttons
btn_virulence = tk.Button(menu_frame, text="Virulence", font=("Arial", 12), width=20, command=virulence_option)
btn_virulence.pack(pady=5)

btn_starting_country = tk.Button(menu_frame, text="Starting Country", font=("Arial", 12), width=20, command=starting_country_option)
btn_starting_country.pack(pady=5)

btn_starting_infected = tk.Button(menu_frame, text="Starting Infected", font=("Arial", 12), width=20, command=starting_infected_option)
btn_starting_infected.pack(pady=5)

btn_start_step = tk.Button(menu_frame, text="Start/Step", font=("Arial", 12), width=20, command=start_step_option)
btn_start_step.pack(pady=5)

btn_reset = tk.Button(menu_frame, text="Reset", font=("Arial", 12), width=20, bg="red", fg="white", command=reset_option)
btn_reset.pack(pady=5)

btn_total_infected = tk.Button(menu_frame, text="Total Infected", font=("Arial", 12), width=20, command=total_infected_option)
btn_total_infected.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()