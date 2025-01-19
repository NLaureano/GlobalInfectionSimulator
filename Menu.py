import tkinter as tk
from tkinter import messagebox

# Function to show information or perform actions
def virulence_option():
    messagebox.showinfo("Virulence", "This will adjust the virulence of the disease.")

def starting_country_option():
    country_window = tk.Toplevel(root)
    country_window.title("Select Starting Country")
    country_window.geometry("300x400")

    countries = ["United States", "Canada", "Brazil", "United Kingdom", "Germany", 
        "France", "India", "Australia", "China", "Russia", "South Africa", "Japan"]
    
    label = tk.Label(country_window, text="Select a country to start infection:", font=("Arial, 12"))
    label.pack(pady=10)

    # Listbox for countries
    country_listbox = tk.Listbox(country_window, font=("Arial", 12), height=10, width=25)
    for country in countries:
        country_listbox.insert(tk.END, country)
    country_listbox.pack(pady=10)

    # Function to handle country selection
    def select_country():
        selected_country = country_listbox.get(tk.ACTIVE)
        messagebox.showinfo("Selected Country", f"You selected {selected_country} as the starting country.")

    # Button to confirm the selection
    select_button = tk.Button(country_window, text="Select", font=("Arial", 12), command=select_country)
    select_button.pack(pady=10)

def starting_infected_option():
    number_window = tk.Toplevel(root)
    number_window.title("Select number of starting infected individuals")
    number_window.geometry("300x400")

    label = tk.Label(number_window, text="Select number of starting infected individuals", font=("Arial, 12"))
    label.pack(pady=10)

    # Listbox for number of starting infectd individuals
    number_listbox = tk.Listbox(number_window, font=("Arial", 12), height=10, width=25)
    for i in range(1, 11):
        number_listbox.insert(tk.END, i*10)
    number_listbox.pack(pady=10)

    # Function to handle country selection
    def select_number():
        selected_number = number_listbox.get(tk.ACTIVE)
        messagebox.showinfo("Selected number", f"You selected {selected_number} as the starting country.")

    # Button to confirm the selection
    select_button = tk.Button(number_window, text="Select", font=("Arial", 12), command=select_number)
    select_button.pack(pady=10)
    
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