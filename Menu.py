import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def open_option1():
    messagebox.showinfo("Option 1", "You selected Option 1!")

def open_option2():
    messagebox.showinfo("Option 2", "You selected Option 2!")

def open_option3():
    messagebox.showinfo("Option 3", "You selected Option 3!")

def quit_app():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Menu Page")
root.geometry("1000x1000")  # Set the window size

# Title Label
title_label = tk.Label(root, text="Welcome to the Menu", font=("Arial", 16), fg="blue")
title_label.pack(pady=20)

# Buttons
btn_option1 = tk.Button(root, text="Option 1", font=("Arial", 12), width=15, command=open_option1)
btn_option1.pack(pady=10)

btn_option2 = tk.Button(root, text="Option 2", font=("Arial", 12), width=15, command=open_option2)
btn_option2.pack(pady=10)

btn_option3 = tk.Button(root, text="Option 3", font=("Arial", 12), width=15, command=open_option3)
btn_option3.pack(pady=10)

btn_exit = tk.Button(root, text="Exit", font=("Arial", 12), width=15, bg="red", fg="white", command=quit_app)
btn_exit.pack(pady=20)

# Run the Tkinter event loop
root.mainloop() 








