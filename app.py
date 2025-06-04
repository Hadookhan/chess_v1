import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("My First App")

# Add a label
label = tk.Label(root, text="Hello, World!")
label.pack()  # Pack the label into the window

# Add a button
button = tk.Button(root, text="Click Me")
button.pack()

# Start the main event loop
root.mainloop()