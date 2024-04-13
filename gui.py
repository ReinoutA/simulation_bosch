import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Create the main window
root = tk.Tk()

# Create a Figure object
fig = Figure(figsize=(5, 5))

# Create an Axes object
ax = fig.add_subplot(111)

# Generate some example data
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)

# Plot the data
ax.plot(x, y)

# Create a canvas for the plot and add it to the main window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Start the Tkinter main loop
root.mainloop()