import tkinter as tk
from tkinter import messagebox

simulation_state = {
    "virulence": 50,
    "starting_country": None,
    "starting_infected": 0,
    "map": "default"
}

infected_count = 0
infected_grids = []

def update_infected_count():
    global infected_count
    infected_count = len(infected_grids)
    total_infected_label.config(f"Total Infected: {infected_count}")

"""
total_infected_label = tk.Label(root, text="Total Infected: 0", font=("Arial", 12))
total_infected_label.pack(pady=10)
"""

def run_simulation():
    #Add simulation function here
    return

# Function to show information or perform actions
def virulence_option():
    # Create a new window for adjusting virulence
    virulence_window = tk.Toplevel(root)
    virulence_window.title("Adjust Virulence")
    virulence_window.geometry("300x200")  # Adjust window size for the slider

    # Label
    label = tk.Label(virulence_window, text="Adjust the virulence:", font=("Arial", 12))
    label.pack(pady=10)

    # Function to update the virulence value when the slider is moved
    def update_virulence(value):
        virulence_label.config(text=f"Virulence: {value}%")

    # Scale (slider) to adjust the virulence value between 0 and 100
    virulence_slider = tk.Scale(virulence_window, from_=0, to=100, orient="horizontal", font=("Arial", 12), command=update_virulence)
    virulence_slider.set(50)  # Set initial value to 50%
    virulence_slider.pack(pady=10)

    # Label to display the current virulence value
    virulence_label = tk.Label(virulence_window, text="Virulence: 50%", font=("Arial", 12))
    virulence_label.pack(pady=10)

    # Button to confirm the selected virulence value
    def confirm_virulence():
        selected_virulence = virulence_slider.get()
        messagebox.showinfo("Virulence Selected", f"You selected {selected_virulence}% virulence.")

    def exit_virulence():
        virulence_window.destroy()

    confirm_button = tk.Button(virulence_window, text="Confirm", font=("Arial", 12), command=confirm_virulence)
    confirm_button.pack(side=tk.LEFT, padx=20, pady=10)

    exit_button = tk.Button(virulence_window, text="Exit", command=exit_virulence)
    exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

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

    def exit_country():
        country_window.destroy()

    # Button to confirm the selection
    select_button = tk.Button(country_window, text="Select", font=("Arial", 12), command=select_country)
    select_button.pack(side=tk.LEFT, padx=20, pady=10)

    exit_button = tk.Button(country_window, text="Exit", command=exit_country)
    exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

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

    def exit_number():
        number_window.destroy()

    # Button to confirm the selection
    select_button = tk.Button(number_window, text="Select", font=("Arial", 12), command=select_number)
    select_button.pack(pady=10)

    exit_button = tk.Button(number_window, text="Exit", command=exit_number)
    exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

def start_step_option():
    run_simulation()


def reset_option():
    #Reset the simulation state
    simulation_state.update({
        "virulence": 0,
        "starting_country": None,
        "starting_infected": 0,
        "map":"default"
    })

def total_infected_option():
    messagebox.showinfo("Total Infected", f"Total infected grids: {infected_count}")
    
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