import tkinter as tk

NUM_MACHINES = 5

def on_button_click():
    label.config(text="Button clicked!")

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f'{screen_width}x{screen_height}')

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# Calculate the center of the screen
center_x = screen_width // 2
center_y = screen_height // 2

# Draw 5 rectangles (boxes) on the canvas
for i in range(NUM_MACHINES):
    top_left_x = center_x - 25  # 25 is half the width of the rectangle
    top_left_y = center_y - 50 * 2 + ((i - NUM_MACHINES // 2) * 100)  # Position the rectangles on top of each other
    bottom_right_x = top_left_x + 100
    bottom_right_y = top_left_y + 50
    canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill="gray")

canvas.create_rectangle(50, 50, 400, screen_height - 100, fill="lightblue")

button = tk.Button(root, text="Simulate", command=on_button_click)
button.pack()

label = tk.Label(root, text="")
label.pack()

root.mainloop()